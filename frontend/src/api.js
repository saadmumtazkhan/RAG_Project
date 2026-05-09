import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const askQuestion = async (question) => {
    const res = await axios.post(`${API_URL}/ask`, {
        question
    });

    return res.data;
};
