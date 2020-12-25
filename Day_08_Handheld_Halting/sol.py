from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, NamedTuple, Set, Tuple


class Instruction(NamedTuple):
    op: str
    value: int

    @classmethod
    def from_string(cls, s: str) -> "Instruction":
        operation, str_value = s.split()
        return cls(op=operation, value=int(str_value))


class ReturnCode(Enum):
    OK = 0
    CYCLED = 1


@dataclass
class Computer:
    instructions: List[Instruction]
    cur_instruction: int
    accumulator: int
    visited: Set[int]

    @classmethod
    def from_text(cls, txt: str) -> "Computer":
        lines = txt.splitlines()
        instructions = [Instruction.from_string(l) for l in lines]
        return cls(
            instructions=instructions, cur_instruction=0, accumulator=0, visited=set()
        )

    def run(self) -> ReturnCode:
        while True:
            if self.cur_instruction == len(self.instructions):
                return ReturnCode.OK
            if self.cur_instruction in self.visited:
                return ReturnCode.CYCLED
            self.visited.add(self.cur_instruction)
            instruction, value = self.instructions[self.cur_instruction]
            if instruction == "nop":
                self.cur_instruction += 1
            elif instruction == "acc":
                self.accumulator += value
                self.cur_instruction += 1
            elif instruction == "jmp":
                self.cur_instruction += value


def run_program(txt: str) -> Tuple[ReturnCode, int]:
    comp = Computer.from_text(txt)
    r = comp.run()
    return r, comp.accumulator


def fix_program(txt: str) -> Tuple[ReturnCode, int]:
    comp = Computer.from_text(txt)
    switchable = [
        i for i, ins in enumerate(comp.instructions) if ins.op in ("jmp", "nop")
    ]
    for s in switchable:
        comp = Computer.from_text(txt)
        op, val = comp.instructions[s]
        comp.instructions[s] = Instruction("jmp" if op == "nop" else "nop", val)

        r = comp.run()
        if r == ReturnCode.OK:
            return r, comp.accumulator
    return ReturnCode.CYCLED, comp.accumulator


text = (Path(__file__).parent / "input.txt").read_text()
test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

_, acc = run_program(test)
assert acc == 5

_, acc = run_program(text)
assert acc == 1671
print(acc)

res, acc = fix_program(test)
assert res == ReturnCode.OK
assert acc == 8

res, acc = fix_program(text)
assert res == ReturnCode.OK
assert acc == 892
print(acc)
