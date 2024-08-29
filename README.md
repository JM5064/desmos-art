# Desmos Art Generator
Creating desmos art from images using lines, circles, and Bézier curves  
( ${\color{red}\text{with color!!}}$ )

## Usage
Clone the git repository
```
git clone https://github.com/JM5064/desmos-art.git
cd desmos-art
```

Run Flask app.py
```python3 app.py```

Open web interface at `http://127.0.0.1:5000`

### Color
After pasting the equations of your graph into Desmos, run the following script in the console of your Desmos page
```js
state = Calc.getState()
var color = "#000000";

for (i=0;i<state.expressions.list.length;i++) {
    if (state.expressions.list[i].latex.startsWith('#')) {
        color = state.expressions.list[i].latex;
    } else {
        state.expressions.list[i].color=color;
    }
}

Calc.setState(state);
```

### Demonstration Videos
- [Mendelssohn Violin Concerto in Desmos](https://youtu.be/xtCtk2-HeUM)
- [Paganini Caprice No. 24 Var. 9 in Desmos](https://youtube.com/shorts/ntZLcAF8ZlY)
- [...👀](https://youtu.be/1IV0sonB-2U)

![Alt text](ex.png)



