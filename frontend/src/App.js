// @flow

import './App.css';
import Chessground from 'react-chessground'
import 'react-chessground/dist/styles/chessground.css'
import React, {useState, useEffect} from "react";
import { Row, Col, Container } from 'react-bootstrap';

function App() {
    const [update, setUpdate] = useState(null);
    const [headers, setHeaders] = useState(null);
    const [lastAnno, setLastAnno] = useState('');
    const [whitePlayer, setWhitePlayer] = useState(null);
    const [blackPlayer, setBlackPlayer] = useState(null);

    function onNewHeaders(headers) {
        setHeaders(headers.headers)
        setBlackPlayer(headers.black)
        setWhitePlayer(headers.white)
    }

    function mount() {
        const evtSource = new EventSource("http://127.0.0.1:8000/status/stream");
        evtSource.addEventListener("update", function(event) {
            // Logic to handle status updates
            let obj = JSON.parse(event.data)
            setUpdate(obj)
            if (obj.anno) {
                setLastAnno(obj.anno)
            }
            });
        evtSource.addEventListener("end", function(event) {
            console.log('Handling end....')
            evtSource.close();
        });
        evtSource.addEventListener("new_game", function(event) {
            console.log('Handling new_game....')
            onNewHeaders(JSON.parse(event.data))
        });

    }
    useEffect(() => {
        mount()}, [])
    console.log(update)
    return (
    <div className="App">
        <Container fluid>
        <Row>
            <Col className="board-col">
                {update ? (
                  <Col lg="6" className="col-4 d-flex justify-content-center text-center">
                      <Row className="board">
                          <Chessground fen={update["fen"]} lastMove={update.uci}/>
                      </Row>
                    </Col>
                  ) : (<></>)}
            </Col>
            <Col className="headers-and-annotation-col">
                {headers && whitePlayer && blackPlayer ? (
                    <Row lg={1} className="text-center">
                        <Row>
                              <Col>
                                  <img src={whitePlayer.image_url} alt={"white"} width="220" height="220" />
                              </Col>
                              <Col>
                              </Col>
                              <Col>
                                  <img src={blackPlayer.image_url} alt={"black"} width="220" height="220" />
                              </Col>
                          </Row>
                          <Row>
                              <Col>
                                  {whitePlayer.name}
                              </Col>
                              <Col>
                                  vs.
                              </Col>
                              <Col>
                                  {blackPlayer.name}
                              </Col>
                          </Row>
                        <Row lg={1} className="headers-and-annotation-col">
                            {headers.date}
                        </Row>
                        <br/>
                        <br/>
                        <br/>
                        <Row lg={1} className="headers-and-annotation-col">
                                Last Annotation:
                        </Row>
                        <Row className="text-center text-wrap annotation">
                            {lastAnno}
                        </Row>
                  </Row>) : (<></>)}
            </Col>
        </Row>
        </Container>
    </div>
    );
}

export default App;