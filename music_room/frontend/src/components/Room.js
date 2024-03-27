import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { Button, ButtonGroup, Grid, Typography } from "@mui/material";

const Room = ({ leaveRoomCallback, roomCode }) => {
    const defaultVotes = 2;

    const [votesToSkip, setVotesToSkip] = useState(defaultVotes);
    const [guestCanPause, setGuestCanPause] = useState(true);
    const [isHost, setIsHost] = useState(false);

    // const location = useLocation();

    //const roomCode = location.pathname.split("/").pop();

    const getRoomDetails = async () => {
        fetch(`/api/get-room?code=${roomCode}`)
            .then((res) => {
                if (!res.ok) {
                    leaveRoomCallback();
                    window.location.href = "/";
                }

                return res.json();
            })
            .then((data) => {
                setVotesToSkip(data.votes_to_skip);
                setGuestCanPause(data.guest_can_pause);
                setIsHost(data.is_host);
            })
            .catch((err) => console.error(err));
    };

    getRoomDetails();

    const onLeaveButtonPress = () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        };

        fetch("/api/leave-room", requestOptions)
            .then((_response) => {
                leaveRoomCallback();
                window.location.href = "/";
            })
            .catch((err) => console.error(err));
    };

    return (
        <>
            <Grid container spacing={1}>
                <Grid item xs={12} align='center'>
                    <Typography variant='h4' component='h4'>
                        Room Code: {roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Typography variant='h6' component='h6'>
                        Votes: {votesToSkip}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Typography variant='h6' component='h6'>
                        Guest Can Pause: {guestCanPause.toString()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Typography variant='h6' component='h6'>
                        Host: {isHost.toString()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Button
                        variant='contained'
                        color='secondary'
                        onClick={onLeaveButtonPress}
                    >
                        Leave Room
                    </Button>
                </Grid>
            </Grid>
        </>
    );
};

export default Room;
