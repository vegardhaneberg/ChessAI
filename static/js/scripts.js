
let config = {
    position: 'start',
    draggable: true,
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
};
let chessboard = ChessBoard("chessboard", config);
let chessgame = new Chess();
let undoMoves = [];
let loading = false;

function onDragStart(source, piece, position, orientation) {
    if (chessgame.game_over() || loading) return false
}

function onDrop(source, target) {
    let move = chessgame.move({
        from: source,
        to: target,
        promotion: 'q', //AutoQueen
    });

    if (chessgame.game_over()){
        document.getElementById('game-over-label').innerHTML = 'Game Over'
    }

    if (move !== null){

    } else {
        return 'snapback'
    }
}

function onSnapEnd () {
    chessboard.position(chessgame.fen());

    let url = "https://9bd5c46620a4.ngrok.io/make_move";
    loading = true;

    $.post(url, {

    });

    //fetch(url).then(response => response.json()).then(data => console.log(data));

    loading = false;
}

$('#backBtn').on('click', function () {
    if (!chessgame.game_over() && !loading){
        let move = chessgame.undo();
        if (move !== null){
            chessboard.position(chessgame.fen());
            undoMoves.push(move);
        }
    }
});

$('#forwardBtn').on('click', function () {
    if (undoMoves.length > 0 && !loading){
        let move = undoMoves.pop();
        chessgame.move(move);
        chessboard.position(chessgame.fen())
    }
});

function sleep (ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}










