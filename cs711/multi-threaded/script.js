let REGISTER_BTN = document.getElementById("register")
let PAIR_BTN = document.getElementById("pair")
let QUIT_GAME_BTN = document.getElementById("quit-game")

let WHOS_MOVE_DISPLAY = document.getElementById("whos-move")
let PLAYING_AS_DISPLAY = document.getElementById("playing-as")
let GAME_STATUS_DISPLAY = document.getElementById("game-status")
let OPPONENT_NAME_DISPLAY = document.getElementById("opponent-name")
let USERNAME_DISPLAY = document.getElementById("username")

const PIECES = {
	"black-bishop": "./assets/black-bishop.png",
	"black-king": "./assets/black-king.png",
	"black-knight": "./assets/black-knight.png",
	"black-pawn": "./assets/black-pawn.png",
	"black-queen": "./assets/black-queen.png",
	"black-rook": "./assets/black-rook.png",
	"white-bishop": "./assets/white-bishop.png",
	"white-king": "./assets/white-king.png",
	"white-knight": "./assets/white-knight.png",
	"white-pawn": "./assets/white-pawn.png",
	"white-queen": "./assets/white-queen.png",
	"white-rook": "./assets/white-rook.png",
}


const setBoard = (game_state) => {
	const board = game_state.board
	for (const square in board) {
		setPiece(square, board[square])
	}
}

const clearBoard = () => {
	document.querySelectorAll(".droppable").forEach(
		(square) => square.innerHTML = ``
	);
}

const setPiece = (square, piece) => {
	let el = document.getElementById(square)
	const img = PIECES[piece]
	el.innerHTML = `<img id="${piece}" draggable="true" class="piece" src=\"${img}\">`
}

const clearPiece = (square) => {
	let el = document.getElementById(square)
	el.innerHTML = ``
}

const movePieceAndUpdateLocalState = (src, dest, piece) => {
	clearPiece(src)
	setPiece(dest, piece)

	// update global state too
	delete GAME_STATE[src]
	GAME_STATE[dest] = piece
}

let GAME_STATE = null;
const resetBoard = () => {
	GAME_STATE = {
		board: {
			// white side
			"a1": "white-rook",
			"b1": "white-knight",
			"c1": "white-bishop",
			"d1": "white-king",
			"e1": "white-queen",
			"f1": "white-bishop",
			"g1": "white-knight",
			"h1": "white-rook",

			"a2": "white-pawn",
			"b2": "white-pawn",
			"c2": "white-pawn",
			"d2": "white-pawn",
			"e2": "white-pawn",
			"f2": "white-pawn",
			"g2": "white-pawn",
			"h2": "white-pawn",

			// black side
			"a8": "black-rook",
			"b8": "black-knight",
			"c8": "black-bishop",
			"d8": "black-king",
			"e8": "black-queen",
			"f8": "black-bishop",
			"g8": "black-knight",
			"h8": "black-rook",

			"a7": "black-pawn",
			"b7": "black-pawn",
			"c7": "black-pawn",
			"d7": "black-pawn",
			"e7": "black-pawn",
			"f7": "black-pawn",
			"g7": "black-pawn",
			"h7": "black-pawn",
		},
		game: null,
		username: null,
		state: null,
		opponent: null,
	}
}


// The state of the chess piece being dragged
let MOVE = { piece: "", src: "", dest: "" }

document.addEventListener("dragstart", event => {
	MOVE.piece = event.target.id
	MOVE.src = event.target.parentElement.id
});

document.addEventListener("dragover", event => {
	event.preventDefault();
	event.dataTransfer.dropEffect = 'move';
});

document.addEventListener("drop", event => {
	event.preventDefault();

	let target = event.target
	if (isElementPiece(event.target)) {
		target = target.parentElement
	}

	MOVE.dest = target.id
	if (MOVE.src !== MOVE.dest) {
		const user = GAME_STATE.username;
		const move = MOVE.src + "_" + MOVE.dest + "_" + MOVE.piece
		fetch(`http://localhost:8080/mymove?player=${GAME_STATE.username}&id=${GAME_STATE.game}&move=${move}`, { keepalive: true })
			.then(
				function(response) {
					if (response.status === 404) {
						QUIT_GAME_BTN.setAttribute("disabled", true)
						PAIR_BTN.removeAttribute("disabled")
						GAME_STATUS_DISPLAY.textContent = "not playing"
						WHOS_MOVE_DISPLAY.textContent = ""
						PLAYING_AS_DISPLAY.textContent = ""
						OPPONENT_NAME_DISPLAY.textContent = ""

						clearBoard()
						resetBoard()
						setBoard(GAME_STATE);
						GAME_STATE.username = user;
					}
					if (response.status !== 200) { // TODO?
						console.log('unexpected status code' + response.status);
						return;
					}

					WHOS_MOVE_DISPLAY.textContent = "their move"
					movePieceAndUpdateLocalState(MOVE.src, MOVE.dest, MOVE.piece)
					setTimeout(pollTheirMove, 1000)
				}
			)
			.catch(function(err) {
				console.log('error issuing request', err);
			});
	}
})

function pollTheirMove() {
	const user = GAME_STATE.username;
	fetch(`http://localhost:8080/theirmove?player=${GAME_STATE.username}&id=${GAME_STATE.game}`, { keepalive: true })
		.then(
			function(response) {
				switch (response.status) {
					case 404:
						QUIT_GAME_BTN.setAttribute("disabled", true)
						PAIR_BTN.removeAttribute("disabled")
						GAME_STATUS_DISPLAY.textContent = "not playing"
						WHOS_MOVE_DISPLAY.textContent = ""
						PLAYING_AS_DISPLAY.textContent = ""
						OPPONENT_NAME_DISPLAY.textContent = ""

						clearBoard()
						resetBoard()
						setBoard(GAME_STATE);
						GAME_STATE.username = user;
					case 423:
						setTimeout(pollTheirMove, 1000);
						return;
					case 200:
						response.json().then(function(data) {
							console.log(data)
							if (data != null) {
								const [src, dest, piece] = data.split("_");
								movePieceAndUpdateLocalState(src, dest, piece);
								WHOS_MOVE_DISPLAY.textContent = "your move"
							}
						});
					default:
						console.log('unexpected status code' + response.status);
						return;
				}
			}
		)
		.catch(function(err) {
			console.log('error issuing request', err);
		});
}

QUIT_GAME_BTN.addEventListener("click", _ => {
	const user = GAME_STATE.username;
	fetch(`http://localhost:8080/quit?player=${user}&id=${GAME_STATE.game}`, { keepalive: true })
		.then(
			function(response) {
				if (response.status !== 200 && response.status != 404) {
					console.log('unexpected status code' + response.status);
					return;
				}

				response.json().then(function(_) {
					QUIT_GAME_BTN.setAttribute("disabled", true)
					PAIR_BTN.removeAttribute("disabled")
					GAME_STATUS_DISPLAY.textContent = "not playing"
					WHOS_MOVE_DISPLAY.textContent = ""
					PLAYING_AS_DISPLAY.textContent = ""
					OPPONENT_NAME_DISPLAY.textContent = ""

					clearBoard()
					resetBoard()
					setBoard(GAME_STATE);
					GAME_STATE.username = user;
				});
			}
		)
		.catch(function(err) {
			console.log('error issuing request', err);
		});

})

PAIR_BTN.addEventListener("click", _ => {
	fetch('http://localhost:8080/pairme?player=' + GAME_STATE.username, { keepalive: true })
		.then(
			function(response) {
				if (response.status === 404) {
					QUIT_GAME_BTN.setAttribute("disabled", true)
					GAME_STATUS_DISPLAY.textContent = "not playing"
					WHOS_MOVE_DISPLAY.textContent = ""
					PLAYING_AS_DISPLAY.textContent = ""
					OPPONENT_NAME_DISPLAY.textContent = ""

					REGISTER_BTN.removeAttribute("disabled");
					USERNAME_DISPLAY.textContent = "";
					PAIR_BTN.addAttribute("disabled", true);

					clearBoard()
					resetBoard()
					setBoard(GAME_STATE);
				}
				if (response.status !== 200) {
					console.log('unexpected status code' + response.status);
					return;
				}

				response.json().then(function(data) {
					QUIT_GAME_BTN.removeAttribute("disabled")
					GAME_STATE.game = data.id
					GAME_STATE.state = data.state
					GAME_STATUS_DISPLAY.textContent = data.state

					if (data.state != "waiting") {
						if ((data.player_1 == GAME_STATE.username) == data.first_players_turn) {
							WHOS_MOVE_DISPLAY.textContent = "your move"
						} else {
							WHOS_MOVE_DISPLAY.textContent = "their move"
							setTimeout(pollTheirMove, 1000)
						}

						PAIR_BTN.setAttribute("disabled", true);

						if (data.player_1 == GAME_STATE.username) {
							PLAYING_AS_DISPLAY.textContent = "playing as WHITE"
							GAME_STATE.opponent = data.player_2
							OPPONENT_NAME_DISPLAY.textContent = `against ${data.player_2}`
						}

						if (data.player_2 == GAME_STATE.username) {
							PLAYING_AS_DISPLAY.textContent = "playing as BLACK"
							GAME_STATE.opponent = data.player_1
							OPPONENT_NAME_DISPLAY.textContent = `against ${data.player_1}`
						}
					}
				});
			}
		)
		.catch(function(err) {
			console.log('error issuing request', err);
		});

})

REGISTER_BTN.addEventListener("click", _ => {
	fetch('http://localhost:8080/register', { keepalive: true })
		.then(
			function(response) {
				if (response.status !== 200) {
					console.log('unexpected status code' + response.status);
					return;
				}

				response.json().then(function(data) {
					USERNAME_DISPLAY.textContent = data.name;
					GAME_STATE.username = data.name;

					REGISTER_BTN.setAttribute("disabled", true);
					PAIR_BTN.removeAttribute("disabled")
				});
			}
		)
		.catch(function(err) {
			console.log('error issuing request', err);
		});
})


const isElementPiece = (el) => {
	return el.classList.contains("piece")
}

resetBoard()
setBoard(GAME_STATE)
