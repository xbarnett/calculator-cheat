import os

class Button:
    def __init__(self, int_op=None, but_op=None, options=1,
                 plus_digit_options=None):
        self.pre_int_operation = int_op
        self.pre_but_operation = but_op
        self.options = options
        self.plus_digit_options = plus_digit_options

    def int_operation(self, a, option):
        if self.pre_int_operation is None:
            return a
        result = self.pre_int_operation(a[0], option)
        try:
            result, locked = result
        except TypeError:
            locked = a[1]
        if result is None:
            return None
        if locked is not None:
            pos, dig, age = locked
            if age == 0:
                locked = None
            else:
                locked = (pos, dig, age - 1)
            digits = str(abs(result))[::-1]
            if len(digits) < pos:
                digits += '0' * (pos - len(digits))
            new_result = int((digits[:pos] + str(dig) + digits[pos+1:])[::-1])
            if result >= 0:
                result = new_result
            else:
                result = -new_result
        if result >= 10 ** 6 or result <= -10 ** 5:
            return None
        return (result, locked)

    def but_operation(self, a, but, option):
        if self.pre_but_operation is None:
            return but
        return self.pre_but_operation(a[0], but, option)
        
    def modify(self, op):
        return self

    def modify_options(self, a):
        if self.plus_digit_options is not None:
            self.options = len(str(abs(a))) + self.plus_digit_options

    def __repr__(self):
        raise NotImplementedError()

class Add(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        return self.a + b

    def modify(self, op):
        return Add(op(self.a))

    def __repr__(self):
        return '|+ {0}|'.format(self.a)

class Multiply(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        return self.a * b

    def modify(self, op):
        return Multiply(op(self.a))

    def __repr__(self):
        return '|* {0}|'.format(self.a)

class Subtract(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        return b - self.a

    def modify(self, op):
        return Subtract(op(self.a))

    def __repr__(self):
        return '|- {0}|'.format(self.a)

class Divide(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        if self.a == 0 or b % self.a != 0:
            return None
        return b // self.a

    def modify(self, op):
        return Divide(op(self.a))

    def __repr__(self):
        return '|/ {0}|'.format(self.a)

class DeleteRightDigit(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        result = abs(a) // 10
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|<<|'

class Insert(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        try:
            return int(str(b) + str(self.a))
        except ValueError:
            return None

    def modify(self, operation):
        return Insert(operation(self.a))

    def __repr__(self):
        return '|{0}|'.format(self.a)

class Replace(Button):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        super().__init__(int_op=self.op)

    def op(self, c, option):
        try:
            return int(str(c).replace(self.a, self.b))
        except ValueError:
            return None

    def __repr__(self):
        return '|{0} => {1}|'.format(self.a, self.b)

class Power(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        if self.a < 0:
            return None
        return b ** self.a

    def __repr__(self):
        return '|x^{0}|'.format(self.a)

class AdditiveInverse(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        return -a

    def __repr__(self):
        return '|+/-|'

class Reverse(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        result = int(str(abs(a))[::-1])
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|Reverse|'

class Sum(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        result = 0
        for digit in str(abs(a)):
            result += int(digit)
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|SUM|'

class ShiftLeft(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        a_str = str(abs(a))
        result = int(a_str[1:] + a_str[0])
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|Shift <|'

class ShiftRight(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        a_str = str(abs(a))
        result = int(a_str[-1] + a_str[:-1])
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|Shift >|'

class Mirror(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        a_str = str(abs(a))
        result = int(a_str + a_str[::-1])
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|Mirror|'

class MetaAdd(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(but_op=self.but_op)

    def op(self, b):
        return self.a + b

    def but_op(self, a, but, option):
        return but.modify(self.op)

    def __repr__(self):
        return '[[+] {0}]'.format(self.a)

class Store(Button):
    def __init__(self, state=None):
        self.state = state
        super().__init__(int_op=self.op, but_op=self.but_op, options=2)

    def op(self, a, option):
        if option == 0:
            if self.state is None:
                return None
            try:
                return int(str(a) + str(self.state))
            except ValueError:
                return None
        else:
            return a

    def but_op(self, a, but, option):
        if option == 0:
            return but
        elif but is self:
            return Store(a)
        else:
            return but
    
    def __repr__(self):
        if self.state is None:
            return '|Store|'
        else:
            return '|{0}|'.format(self.state)

class Inv10(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        result = ''
        for digit in str(abs(a)):
            if digit == '0':
                result += '0'
            else:
                result += str(10 - int(digit))
        result = int(result)
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|Inv10|'

class ABC(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        return None
        
    def __repr__(self):
        return '|ABC|'

class SortAscending(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        result = int(''.join(sorted(str(abs(a)))))
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|SORT >|'
    
class SortDescending(Button):
    def __init__(self):
        super().__init__(int_op=self.op)

    def op(self, a, option):
        result = int(''.join(sorted(str(abs(a)), reverse=True)))
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|SORT <|'

class Cut(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op)

    def op(self, b, option):
        result = str(b).replace(str(self.a), '')
        if result in ('', '-'):
            return 0
        return int(result)

    def modify(self, op):
        return Cut(op(self.a))

    def __repr__(self):
        return '|CUT {0}|'.format(self.a)

class Delete(Button):
    def __init__(self):
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, a, option):
        digit_list = list(str(abs(a)))
        del digit_list[-option - 1]
        result = ''.join(digit_list)
        if result == '':
            result = '0'
        result = int(result)
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|DELETE|'

class InsertOptions(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op, plus_digit_options=1)

    def op(self, b, option):
        dig_list = str(abs(b))[::-1]
        try:
            result = int((dig_list[:option] + str(self.a) +
                          dig_list[option:])[::-1])
        except ValueError:
            return None
        if b >= 0:
            return result
        else:
            return -result

    def modify(self, op):
        return InsertOptions(op(self.a))

    def __repr__(self):
        return '|INSERT {0}|'.format(self.a)

class Round(Button):
    def __init__(self):
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, a, option):
        result = abs(a)
        option = 10 ** option
        remainder = a % option
        result -= remainder
        if remainder * 2 >= option:
            result += option
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '|ROUND|'

class AddOptions(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, b, option):
        digits = str(abs(b))[::-1]
        new_digit = str((int(digits[option]) + self.a) % 10)
        result = int((digits[:option] + new_digit + digits[option + 1:])[::-1])
        if b >= 0:
            return result
        else:
            return -result

    def modify(self, op):
        return AddOptions(op(self.a))

    def __repr__(self):
        return '[_+ {0}]'.format(self.a)

class SubtractOptions(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, b, option):
        digits = str(abs(b))[::-1]
        new_digit = str((int(digits[option]) - self.a) % 10)
        result = int((digits[:option] + new_digit + digits[option + 1:])[::-1])
        if b >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '[_- {0}]'.format(self.a)

class Shift(Button):
    def __init__(self):
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, a, option):
        digits = str(abs(a))
        result_digits = digits[option:] + digits[:option]
        if result_digits == '':
            result = 0
        else:
            result = int(result_digits)
        if a >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '[SHIFT]'

class ReplaceOptions(Button):
    def __init__(self, a):
        self.a = a
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, b, option):
        digits = str(abs(b))[::-1]
        result = int((digits[:option] + str(self.a) + digits[option + 1:])
                     [::-1])
        if b >= 0:
            return result
        else:
            return -result

    def __repr__(self):
        return '[_{0}]'.format(self.a)

class Lock(Button):
    def __init__(self):
        super().__init__(int_op=self.op, plus_digit_options=0)

    def op(self, a, option):
        digits = str(abs(a))[::-1]
        locked_digit = digits[option]
        return (a, (option, locked_digit, 1))

    def __repr__(self):
        return '[Lock]'
    
class Level:
    def __init__(self, start, goals, moves, buttons, portal=None):
        self.start = start
        self.goals = goals
        self.moves = moves
        self.buttons = buttons
        self.portal = portal

    def portalify(self, a):
        if self.portal is None:
            return a
        (lower, upper) = self.portal
        lower = 10**lower
        upper = 10**upper
        n = abs(a)
        while n >= upper:
            top = n//upper
            n %= upper
            n += (top%10)*lower+(top//10)*upper
        if a >= 0:
            return n
        else:
            return -n

    def solve_iter(self, start, moves, move_list, buttons, goal, is_str):
        if start[0] == goal:
            if is_str:
                for button in buttons:
                    if isinstance(button, ABC):
                        return move_list
            else:
                return move_list
        if moves == 0:
            return None
        for button in buttons:
            button.modify_options(start[0])
            for option in range(button.options):
                new_start = button.int_operation(start, option)
                if new_start is None:
                    continue
                new_start = (self.portalify(new_start[0]), new_start[1])
                new_buttons = []
                for b in buttons:
                    new_button = button.but_operation(start, b, option)
                    new_buttons.append(new_button)
                solution = self.solve_iter(new_start, moves-1,
                                           move_list + [(button, option)],
                                           new_buttons, goal, is_str)
                if solution is not None:
                    return solution
        return None

    def intify(self, goal):
        result = 0
        for letter in goal:
            result *= 10
            result += (ord(letter)-ord('A'))//3+1
        return result
    
    def solve(self):
        solutions = []
        for goal in self.goals:
            solution = None
            is_str = isinstance(goal, str)
            if is_str:
                if self.moves == 0:
                    solutions.append(None)
                    continue
                else:
                    moves = self.moves - 1
                goal = self.intify(goal)
            else:
                moves = self.moves
            while True:
                next_solution = self.solve_iter((self.start, None), moves, [],
                                                self.buttons, goal, is_str)
                if next_solution is None:
                    break
                solution = next_solution
                if solution == []:
                    break
                moves = len(solution) - 1
            if is_str:
                if solution is not None:
                    solution.append((ABC(), 0))
            solutions.append(solution)
        return solutions

    def __repr__(self):
        return ('Start: {0}\nGoals: {1}\nMoves: {2}\nButtons: {3}\n'+
                'Portal: {4}\n').format(self.start, self.goals, self.moves,
                                        self.buttons, self.portal)

def string_to_button(s):
    try:
        int(s)
        is_int = True
    except ValueError:
        is_int = False
    if s == '+/-':
        return AdditiveInverse()      
    elif s[0] == '+':
        a = int(s[1:])
        return Add(a)
    elif s[0] == '*':
        a = int(s[1:])
        return Multiply(a)
    elif s[0] == '-':
        a = int(s[1:])
        return Subtract(a)
    elif s[0] == '/':
        a = int(s[1:])
        return Divide(a)
    elif s == '<<':
        return DeleteRightDigit()
    elif is_int:
        return Insert(int(s))
    elif '=>' in s:
        i = s.find('=>')
        a = s[:i]
        b = s[i+2:]
        return Replace(a, b)
    elif s[:2] == 'x^':
        a = int(s[2:])
        return Power(a)
    elif s == 'Reverse':
        return Reverse()
    elif s == 'SUM':
        return Sum()
    elif s == 'Shift<':
        return ShiftLeft()
    elif s == 'Shift>':
        return ShiftRight()
    elif s == 'Mirror':
        return Mirror()
    elif s[:3] == '[+]':
        a = int(s[3:])
        return MetaAdd(a)
    elif s[:5] == 'Store':
        if s[5:] == '':
            return Store()
        else:
            a = int(s[5:])
            return Store(a)
    elif s == 'Inv10':
        return Inv10()
    elif s == 'ABC':
        return ABC()
    elif s == 'SORT>':
        return SortAscending()
    elif s == 'SORT<':
        return SortDescending()
    elif s[:3] == 'CUT':
        a = int(s[3:])
        return Cut(a)
    elif s == 'DELETE':
        return Delete()
    elif s[:6] == 'INSERT':
        a = int(s[6:])
        return InsertOptions(a)
    elif s == 'ROUND':
        return Round()
    elif s[:2] == '_+':
        a = int(s[2:])
        return AddOptions(a)
    elif s[:2] == '_-':
        a = int(s[2:])
        return SubtractOptions(a)
    elif s == 'SHIFT':
        return Shift()
    elif s[0] == '_':
        a = int(s[1:])
        return ReplaceOptions(a)
    elif s == 'LOCK':
        return Lock()
    else:
        raise ValueError('unknown button')    

def interactive_session():
    while True:
        level_number = input('Level number: ')
        level_file = open(os.path.join('levels2', level_number), 'w')
        start = int(input('Start: '))
        goals = input('Goals: ').split()
        for (i, g) in enumerate(goals):
            try:
                goals[i] = int(g)
            except ValueError:
                goals[i] = g.upper()
        moves = int(input('Moves: '))
        portal = input('Portal: ')
        if portal == '':
            portal = None
        else:
            (lower, upper) = portal.split()
            portal = (int(lower), int(upper))
        buttons = []
        while True:
            button_string = input('Button: ')
            if button_string == '':
                break
            buttons.append(string_to_button(button_string))
        level = Level(start, goals, moves, buttons, portal)
        level_file.write(repr(level))
        solutions = level.solve()
        for solution in solutions:
            if solution == None:
                print('NO SOLUTION')
            else:
                for (button, option) in solution:
                    if option == 0:
                        opsym = ''
                    else:
                        opsym = str(option)
                    print(opsym+repr(button), end=', ')
                print()
        level_file.write(repr(solutions)+'\n')
        level_file.close()
        print()

if __name__ == '__main__':
    interactive_session()
