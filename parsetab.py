
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'DIVIDE EQUALS LPAREN MINUS NAME NUMBER PLUS RPAREN TIMESstatement : NAME EQUALS expressionexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDE expressionexpression : LPAREN expression RPARENexpression : NUMBERexpression : NAME'
    
_lr_action_items = {'NAME':([0,3,6,8,9,10,11,],[2,4,4,4,4,4,4,]),'$end':([1,4,5,7,13,14,15,16,17,],[0,-8,-1,-7,-2,-3,-4,-5,-6,]),'EQUALS':([2,],[3,]),'LPAREN':([3,6,8,9,10,11,],[6,6,6,6,6,6,]),'NUMBER':([3,6,8,9,10,11,],[7,7,7,7,7,7,]),'PLUS':([4,5,7,12,13,14,15,16,17,],[-8,8,-7,8,8,8,8,8,-6,]),'MINUS':([4,5,7,12,13,14,15,16,17,],[-8,9,-7,9,9,9,9,9,-6,]),'TIMES':([4,5,7,12,13,14,15,16,17,],[-8,10,-7,10,10,10,10,10,-6,]),'DIVIDE':([4,5,7,12,13,14,15,16,17,],[-8,11,-7,11,11,11,11,11,-6,]),'RPAREN':([4,7,12,13,14,15,16,17,],[-8,-7,17,-2,-3,-4,-5,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([3,6,8,9,10,11,],[5,12,13,14,15,16,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> NAME EQUALS expression','statement',3,'p_statement_assign','EditorTextoPython.py',59),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','EditorTextoPython.py',63),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','EditorTextoPython.py',64),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','EditorTextoPython.py',65),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','EditorTextoPython.py',66),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','EditorTextoPython.py',73),
  ('expression -> NUMBER','expression',1,'p_expression_number','EditorTextoPython.py',77),
  ('expression -> NAME','expression',1,'p_expression_name','EditorTextoPython.py',81),
]
