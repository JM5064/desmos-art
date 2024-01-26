var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);

lines = equations.split('\n');
console.log(lines.length)

for (var i = 0; i < lines.length; i++) {
    calculator.setExpression({ id: i, color: null, latex: lines[i] });
}


state = calculator.getState();

var color = "#000000";

for (i=0;i<state.expressions.list.length;i++) {
    var equation = state.expressions.list[i].latex;
    if (equation !== undefined && equation.startsWith('#')) {
        color = state.expressions.list[i].latex;
    }
    state.expressions.list[i].color=color;
}

calculator.setState(state);

calculator.setMathBounds({
    left: -75.065,
    right: 1405.354,
    bottom: -161.045,
    top: 934.883
  });
