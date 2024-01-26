var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);

lines = equations.split('\n');

var color = '#000000';

for (var i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('#')) {
        color = lines[i];
    } else {
        calculator.setExpression({ id: i, color: color, latex: lines[i] });
    }
}

calculator.setMathBounds({
    left: -75.065,
    right: 1405.354,
    bottom: -161.045,
    top: 934.883
  });
