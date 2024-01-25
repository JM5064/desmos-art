var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);

state = calculator.getState()

var color = "#000000";

for (i=0;i<state.expressions.list.length;i++) {
    var equation = state.expressions.list[i].latex;
    if (equation !== undefined && equation.startsWith('#')) {
        color = state.expressions.list[i].latex;
    }
    state.expressions.list[i].color=color
}

Calc.setState(state);