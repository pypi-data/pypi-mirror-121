from argparse import ArgumentParser
from dataclasses import dataclass
from importlib.resources import open_text
from pathlib import Path
from re import match
from shutil import move
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import IO, List, Optional, Tuple

from naughtty import NaughTTY
from thtml import Scope, write_html
from yaml import safe_load

from dinject.enums import Emit, Emitted, Host
from dinject.executors import get_executor
from dinject.types import Instruction
from dinject.version import get_version


@dataclass
class Block:
    complete: bool
    language: str
    lines: List[str]

    def get_script(self) -> str:
        return "".join(self.lines)

    def set_script(self, script: str) -> None:
        self.lines = [script]


def dinject_file(path: Path) -> None:
    """
    Executes the code blocks and injects the results into the Markdown document
    at `path`.
    """

    block: Optional[Block] = None
    skip_to_emitted_end = False

    with NamedTemporaryFile("a", delete=False) as t:
        with open(path, "r") as p:
            for line in p:
                din = is_instruction(line)

                if skip_to_emitted_end:
                    if din and din.emitted == Emitted.END:
                        skip_to_emitted_end = False
                    continue

                if din and block:
                    execute(block=block, instruction=din, writer=t)
                    block = None
                    if din.emitted == Emitted.START:
                        skip_to_emitted_end = True
                    continue

                t.write(line)

                if block:
                    if not block.complete:
                        if line == "```\n":
                            block.complete = True
                            continue

                        block.lines.append(line)
                        continue

                else:
                    block = is_block_start(line)
                    continue

        t.flush()
        move(t.name, path)


def execute(block: Block, instruction: Instruction, writer: IO[str]) -> None:
    """Execute the script then write the result."""

    executor_type = get_executor(block.language)

    if not executor_type:
        # We don't support this language, so pass through.
        write_block(block, writer)
        return

    executor = executor_type(block.get_script())

    if instruction.host == Host.TERMINAL:
        n = NaughTTY(command=executor.arguments)
        n.execute()
        content = n.output
    else:
        process = run(executor.arguments, capture_output=True)
        content = process.stdout.decode("UTF-8")

    instruction.write_emitted_start(writer)

    if instruction.emit == Emit.HTML:
        print("html")
        with open_text(__package__, "thtml-theme.yml") as t:
            theme = safe_load(t)
        write_html(text=content, writer=writer, scope=Scope.FRAGMENT, theme=theme)
    else:
        print("md")
        result = Block(complete=True, language="text", lines=[content])
        write_block(result, writer)

    instruction.write_emitted_end(writer)


def is_block_start(line: str) -> Optional[Block]:
    m = match("^```(.+)$", line)
    if not m:
        return None
    return Block(language=m.group(1), lines=[], complete=False)


def is_instruction(line: str) -> Optional[Instruction]:
    """
    If `line` is an instruction then deserialises and returns it, otherwise
    returns `None`.
    """

    m = match("^<!--dinject(.*)-->$", line)
    if not m:
        return None
    return Instruction.parse(m.group(1))


def make_response(cli_args: Optional[List[str]] = None) -> Tuple[str, int]:
    """Makes a response to the given command line arguments."""

    parser = ArgumentParser(
        description="Executes Markdown code blocks and injects the results.",
        epilog="Made with love by Cariad Eccleston: https://github.com/cariad/dinject",
    )

    parser.add_argument("files", help="Markdown files", nargs="*")

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the version",
    )

    args = parser.parse_args(cli_args)

    if args.version:
        return get_version(), 0

    if not args.files:
        return "You must specify at least one Markdown file.", 1

    for file in args.files:
        dinject_file(Path(file))

    return "", 0


def write_block(block: Block, writer: IO[str]) -> None:
    """Writes a Markdown code block."""

    writer.write(f"```{block.language}\n")
    writer.write("".join(block.get_script()))
    writer.write("```\n\n")
