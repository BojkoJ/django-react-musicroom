import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";
import RoomJoinPage from "./RoomJoinPage";
import RoomCreatePage from "./RoomCreatePage";

const HomePage = () => {
    return (
        <Router>
            <Switch>
                <Route exact path='/'>
                    <p>This is the home page</p>
                </Route>
                <Route path='/join'>
                    <RoomJoinPage />
                </Route>
                <Route path='/create'>
                    <RoomCreatePage />
                </Route>
            </Switch>
        </Router>
    );
};

export default HomePage;
