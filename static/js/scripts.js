
let config = {
    position: 'start',
    draggable: true,
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    onMouseoverSquare: onMouseoverSquare,
    onMouseoutSquare: onMouseoutSquare,
};
let chessboard = ChessBoard("chessboard", config);
let chessgame = new Chess();
let undoMoves = [];
let loading = false;
var whiteSquareGrey = '#a9a9a9'
var blackSquareGrey = '#696969'

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

async function onSnapEnd () {
    chessboard.position(chessgame.fen());

    loading = true;
    document.getElementById("loader-image").style.opacity = "1";
    await $.ajax({
        type: "POST",
        url: "/make_move",
        data: {param: chessgame.fen()}
    }).done(function (response) {
        chessgame.move(response, { sloppy: true })
        chessboard.position(chessgame.fen());
    });
    document.getElementById("loader-image").style.opacity = "0";

    loading = false;
}

$('#backBtn').on('click', function () {
    if (!chessgame.game_over() && !loading){
        let blackMove = chessgame.undo();
        let whiteMove = chessgame.undo();
        if (whiteMove !== null){
            chessboard.position(chessgame.fen());
            undoMoves.push(blackMove);
            undoMoves.push(whiteMove);
        }
    }
});

$('#forwardBtn').on('click', function () {
    if (undoMoves.length > 1 && !loading){
        let whiteMove = undoMoves.pop();
        let blackMove = undoMoves.pop();
        chessgame.move(whiteMove);
        chessboard.position(chessgame.fen())
        chessgame.move(blackMove);
        chessboard.position(chessgame.fen())
    }
});

$('#resign-button').on('click', function () {
    chessgame = new Chess();
    chessboard.position(chessgame.fen())
});

function onMouseoverSquare(square, piece){
    let moves = chessgame.moves({
        square: square,
        verbose: true
    });

    if (moves.length === 0) return

    highlightSquare(square)

    for (var i = 0; i < moves.length; i++){
        highlightSquare(moves[i].to)
    }

}

function onMouseoutSquare (square, piece) {
    removeGreySquares()
}

function removeGreySquares () {
    $('#chessboard .square-55d63').css('background', '')
}

function highlightSquare (square) {
    var $square = $('#chessboard .square-' + square)
  
    var background = whiteSquareGrey
    if ($square.hasClass('black-3c85d')) {
      background = blackSquareGrey
    }
  
    $square.css('background', background)
}


function sleep (ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}











