import React, { useState } from "react";
import { useLocation } from "react-router-dom";

const Room = () => {
    const defaultVotes = 2;

    const [votesToSkip, setVotesToSkip] = useState(defaultVotes);
    const [guestCanPause, setGuestCanPause] = useState(true);
    const [isHost, setIsHost] = useState(false);

    const location = useLocation();

    const roomCode = location.pathname.split("/").pop();

    const getRoomDetails = async () => {
        fetch(`/api/get-room?code=${roomCode}`)
            .then((res) => res.json())
            .then((data) => {
                setVotesToSkip(data.votes_to_skip);
                setGuestCanPause(data.guest_can_pause);
                setIsHost(data.is_host);
            })
            .catch((err) => console.error(err));
    };

    getRoomDetails();

    return (
        <div>
            <h3>{roomCode}</h3>
            <p>Votes: {votesToSkip}</p>
            <p>Guest Can Pause: {guestCanPause.toString()}</p>
            <p>Host: {isHost.toString()}</p>
        </div>
    );
};

export default Room;
