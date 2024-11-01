let elt = document.getElementById('calculator');
let calculator = Desmos.GraphingCalculator(elt);
let imageCount = 0;


function setBounds() {
    calculator.setMathBounds({ 
        left: -52.57549,
        right: 543.70496, 
        bottom: -88.3414,
        top: 353.07429
      });

}

setBounds();

setupBezierDefinition();
let defaultState = calculator.getState();
let pass = 0;
let imageChunks = 4;
let totalTime = 0;


function setupBezierDefinition() {
    calculator.setExpression({ latex: `p_{12}(t, p_a, p_b) = (1-t)p_a+tp_b` });
    calculator.setExpression({ latex: `p_{23}(t, p_b, p_c) = (1-t)p_b+tp_c` });
    calculator.setExpression({ latex: `p_{34}(t, p_c, p_d) = (1-t)p_c+tp_d` });
    calculator.setExpression({ latex: `p_{123}(t, p_a, p_b, p_c) = (1-t)p_{12}(t, p_a, p_b) + tp_{23}(t, p_b, p_c)` });
    calculator.setExpression({ latex: `p_{234}(t, p_b, p_c, p_d) = (1-t)p_{23}(t, p_b, p_c) + tp_{34}(t, p_c, p_d)` });
    calculator.setExpression({ latex: `p_{1234}(t, p_a, p_b, p_c, p_d) = (1-t)p_{123}(t, p_a, p_b, p_c) + tp_{234}(t, p_b, p_c, p_d)` });
}


async function drawLines(lines) {
    let startTime = performance.now()
    let color = '#000000';

    let start = pass * Math.floor(lines.length / imageChunks);
    let end = (pass + 1) * Math.floor(lines.length / imageChunks);

    if (start == 0) {
        start = 6;
    }

    for (let i = start; i < end; i++) {
        if (lines[i].startsWith('#')) {
            color = lines[i];
        } else {
            calculator.setExpression({ color: color, latex: lines[i] });
        }
    }

    pass++;

    const elapsedTime = performance.now() - startTime;
    console.log(start + " " + end);
    totalTime += elapsedTime;
}


async function takeScreenshot() {
    let opts = {
        "mode": "contain",
        "width": window.screen.width,
        "height": window.screen.height,
        "targetPixelRatio": 2,
        "preserveAxisNumers": false
    };

    await new Promise((resolve) => {
        calculator.asyncScreenshot(opts, async (result) => {
            await downloadImage(result);
            resolve();
        });
    })
    
}


async function downloadImage(imageData) {
    let img = document.createElement('a');
    img.style.display = 'none';
    
    img.href = imageData;

    img.download = "wuv_" + imageCount + '.png';
    imageCount++;

    document.body.appendChild(img);

    img.click();

    document.body.removeChild(img);  
}

async function removeLines() {
    calculator.setState(defaultState);
}


async function processEquations() {
    const chunkSize = 10;
    const totalChunks = Math.ceil(equations.length / chunkSize);

    for (let i = 0; i < totalChunks; i++) {
        const start = chunkSize * i;
        const end = Math.min(start + chunkSize, equations.length);
        const chunk = equations.slice(start, end);

        await processChunk(chunk);
    }
}

async function processChunk(chunk) {
    for (const equations of chunk) {
        await drawLines(equations);
        await takeScreenshot();
        await removeLines();

        if (pass > imageChunks - 1) {
            pass = 0;
            console.log("Total Time: " + totalTime);
        }
    }
}


async function startProcess() {
    for (let i = 0; i < imageChunks; i++) {
        await processEquations();
    }
}

startProcess();

