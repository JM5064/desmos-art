var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);


function setBounds() {
    calculator.setMathBounds({
        left: -75.065,
        right: 1405.354,
        bottom: -161.045,
        top: 934.883
      });
}

setBounds();


async function drawLines(lines) {
    return new Promise(async resolve => {
        console.log("hello");

        // lines = equations[img];
    
        var color = '#000000';
    
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].startsWith('#')) {
                color = lines[i];
            } else {
                calculator.setExpression({ id: i, color: color, latex: lines[i] });
            }
        }
    
        await takeScreenshot();
        resolve();
    });
    
}


async function takeScreenshot() {
    return new Promise(async resolve => {
        var opts = {
            "mode": "contain",
            "width": window.screen.width,
            "height": window.screen.height,
            "targetPixelRatio": 1,
            "preserveAxisNumers": false
        };
    
        var data = await calculator.asyncScreenshot(opts, downloadImage);
        await removeLines();
        resolve();
    })

    
}


async function downloadImage(imageData) {
    return new Promise(async resolve => {
        var img = document.createElement('a');
        img.style.display = 'none';
        
        img.href = imageData;
    
        img.download = 'image.jpg';
    
        document.body.appendChild(img);
    
        img.click();
    
        document.body.removeChild(img);
    
        // await removeLines();
        resolve();
    })
    
}

async function removeLines() {
    return new Promise(async resolve => {
        var expressions = calculator.getExpressions();
        for (var i = 0; i < expressions.length; i++) {
            calculator.removeExpression({ id: expressions[i].id})
        }
        resolve();
    })
}


async function processEquations() {
    for (var img = 0; img < equations.length; img++) {
        await drawLines(equations[img]);
    }
    
    // for await (lines of equations) {
    //     await drawLines(lines);
    // }
    console.log("are you waiting?")
}

processEquations();





