import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";
import Room from "./Room";
import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";

const HomePage = () => {
    return (
        <Router>
            <Switch>
                <Route exact path='/'>
                    <p>This is the home page</p>
                </Route>
                <Route path='/join'>
                    <JoinRoomPage />
                </Route>
                <Route path='/create'>
                    <CreateRoomPage />
                </Route>
                <Route path='/room/:roomCode'>
                    <Room />
                </Route>
            </Switch>
        </Router>
    );
};

export default HomePage;
