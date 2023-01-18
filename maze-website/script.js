(async () => {
    try {
        const rawResponse = await fetch(`http://localhost:3000/get-maze`); // requests json from http server
        var data = await rawResponse.json();
    }
    catch (err) {
        alert('Cannot reach server.\n\n' + err)
    }

    maze_height = data.hw[0]
    maze_width = data.hw[1]

    maze_array = [] // 2D array of all squares
    rows_array = []

    function drawMaze(width, height) { // (int, int) 

        for (let i = 0; i < maze_array.length; i++) {
            for (let j = 0; j < maze_array[i].length; j++) {
                maze_array[i][j].remove()
            }
        }

        for (let i = 0; i < rows_array.length; i++) {
            rows_array[i].remove()
        }
        maze_array = []


        // Adds divs (squares) to html, creates maze
        maze_length_pixels = window.innerHeight > window.innerWidth ? window.innerWidth : window.innerHeight;
        maze_length_pixels *= 0.8

        for (let row = 0; row < height; row++) {

            row_array = []
            row_div = document.createElement('div')
            row_div.classList.add('mazerow')
            row_div.style.height = `${maze_length_pixels / height}px`

            for (let col = 0; col < width; col++) {

                square = document.createElement('div')
                square.classList.add('mazesquare', `${row},${col}`)
                square.style.height = `${maze_length_pixels / height}px`
                square.style.width = `${maze_length_pixels / width}px`


                row_array.push(square)
                row_div.appendChild(square)
            }
            maze_array.push(row_array)
            rows_array.push(row_div)
            document.getElementById('maze').appendChild(row_div)
        }
    }
    drawMaze(maze_width, maze_height)

    function drawFromArray(array, colors) { // ([], {})
        // Draws maze walls based on a 2D Array
        for (let row = 0; row < array.length; row++) {
            for (let col = 0; col < array[row].length; col++) {
                maze_array[row][col].style.backgroundColor = colors[array[row][col]]
            }
        }
    }
    drawFromArray(data.maze, { 0: 'white', 1: 'black', 2: 'green', 3: 'yellow' })

    function drawCoords(coords, color) {  // ([], str)
        // Draws any passed coordinates (in this case the path) in any given colour
        console.log(coords)
        for (let i = 0; i < coords.length; i++) {
            setTimeout(() => {
                square = document.getElementsByClassName(`${coords[i][0]},${coords[i][1]}`)[0]
                square.style.transition = '0.2s'
                square.style.backgroundColor = color;
            }, 20 * i)
        }
    }

    button = document.getElementById('solve-button')
    function handleSolveButton() {
        // On 'solve' button press
        try {
            drawCoords(data.path, 'red')
        }
        catch {
            alert('Path invalid.')
        }
    }
    button.onclick = function () { handleSolveButton(data.path) }

    function getData() {
        return data.path
    }

    async function listenForNewMaze() {
        // Waits for server to respond with a new maze, when it is updated (12 hours max)
        const rawResponse = await fetch(`http://localhost:3000/listen-for-maze`);
        data = await rawResponse.json();

        try {
            drawMaze(data.hw[1], data.hw[0])
            drawFromArray(data.maze, { 0: 'white', 1: 'black', 2: 'green', 3: 'yellow' })
            //setTimeout(() => {
            //    drawCoords(data.path, 'red')
            //}, 1000)
        }
        catch (err) {
            alert('Recieved invalid maze from server.\n\n' + err)
        }

        listenForNewMaze()
    }
    listenForNewMaze()

})();

// <3