// @flow

import './App.css';
import Chessground from 'react-chessground'
import 'react-chessground/dist/styles/chessground.css'
import React, {useEffect, useState} from "react";
import {Col, Row} from 'react-bootstrap';

function App() {
    const [update, setUpdate] = useState(null);
    const [headers, setHeaders] = useState(null);
    const [lastMove, setLastMove] = useState([]);
    const [lastAnno, setLastAnno] = useState('');
    const [currentFen, setCurrentFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR');
    const [whitePlayer, setWhitePlayer] = useState(null);
    const [blackPlayer, setBlackPlayer] = useState(null);

    function onNewHeaders(headers) {
        console.log(JSON.stringify(headers))
        setHeaders(headers.headers)
        setBlackPlayer(headers.black)
        setWhitePlayer(headers.white)
        setLastAnno('')
        setLastMove([])
        setCurrentFen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    }

    function mount() {
        const evtSource = new EventSource("http://127.0.0.1:8000/status/stream");
        evtSource.addEventListener("update", function (event) {
            // Logic to handle status updates
            let obj = JSON.parse(event.data)
            setUpdate(obj)
            setLastAnno(obj.anno)
            setLastMove(obj.uci)
            if (obj.fen) {
                setCurrentFen(obj.fen)
            }
        });
        evtSource.addEventListener("end", function (event) {
            console.log('Handling end....')
            evtSource.close();
        });
        evtSource.addEventListener("new_game", function (event) {
            console.log('Handling new_game....')
            onNewHeaders(JSON.parse(event.data))
        });

    }

    useEffect(() => {
        mount()
    }, [])
    return (
        <div className="App">
            <Row className="main-row">
                <div className="board-col">
                    <Col lg="6" className="col-4 d-flex justify-content-center text-center">
                        <Row className="board">
                            <Chessground fen={currentFen} lastMove={lastMove}/>
                        </Row>
                    </Col>
                </div>
                <div className="photos">
                    {headers && whitePlayer && blackPlayer ? (
                        <>
                            <Row>
                                <img
                                    src={blackPlayer.image_url.startsWith("http://www.osimira") ? 'hoodie_guy.jpg' : blackPlayer.image_url}
                                    alt={"black"} width="180" height="180"/>
                            </Row>
                            <Row className="names">
                                {blackPlayer.name}
                            </Row>
                            <Row>
                                <img
                                    src={whitePlayer.image_url.startsWith("http://www.osimira") ? 'hoodie_guy.jpg' : whitePlayer.image_url}
                                    alt={"white"} width="180" height="180"/>
                            </Row>
                            <Row className="names">
                                {whitePlayer.name}
                            </Row>
                        </>
                    ) : (<></>)}

                </div>
                <div className="headers-and-annotation-col">
                    {headers && whitePlayer && blackPlayer ? (
                        <div>
                            <Row className="date">
                                {headers.combined}
                            </Row>
                            <Row className="text-center text-wrap annotation">
                                {lastAnno}
                            </Row>
                        </div>) : (<></>)}
                </div>
            </Row>
        </div>
    );
}

export default App;
