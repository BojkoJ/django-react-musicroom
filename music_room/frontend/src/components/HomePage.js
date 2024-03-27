import React, { useState } from "react";
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
import { Button, ButtonGroup, Grid, Typography } from "@mui/material";

const HomePage = () => {
    const [roomCode, setRoomCode] = useState(null);

    const renderHomePage = () => {
        return (
            <Grid container spacing={3}>
                <Grid item xs={12} align='center'>
                    <Typography variant='h3' component='h3'>
                        Music Room
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <ButtonGroup
                        disableElevation
                        variant='contained'
                        color='primary'
                        style={{
                            display: "flex",
                            justifyContent: "space-around",
                            width: "350px",
                        }}
                    >
                        <Button
                            color='primary'
                            to='/join'
                            component={Link}
                            style={{ borderRadius: "5px" }}
                        >
                            Join a Room
                        </Button>

                        <Button
                            color='secondary'
                            to='/create'
                            component={Link}
                            style={{ borderRadius: "5px" }}
                        >
                            Create a Room
                        </Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
        );
    };

    const componentDidMount = async () => {
        fetch("/api/user-in-room")
            .then((response) => response.json())
            .then((data) => {
                setRoomCode(data.code);
                console.log(data.code);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    };

    componentDidMount();

    return (
        <Router>
            <Switch>
                <Route
                    exact
                    path='/'
                    render={() => {
                        return roomCode ? (
                            <Redirect to={`/room/${roomCode}`} />
                        ) : (
                            renderHomePage()
                        );
                    }}
                ></Route>

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
