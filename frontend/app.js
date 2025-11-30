

const workoutForm = document.getElementById("workout-form");
workoutForm.onsubmit = function (event) {
    event.preventDefault();

    const workoutType = document.getElementById("type").value;
    const workoutDuration = Number(document.getElementById("duration").value);
    const moodNumber = Number(document.getElementById("mood").value);
    const dateInput = document.getElementById("date").value;
    const performedAt = new Date(dateInput).toISOString();

    const payload = {
        type: workoutType,
        duration_minutes: workoutDuration,
        mood_number: moodNumber,
        performed_at: performedAt,
        notes: null
    };

    console.log("Payload ready:", payload);
    workoutForm.reset();
};

