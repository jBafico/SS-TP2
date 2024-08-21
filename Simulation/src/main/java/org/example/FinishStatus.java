package org.example;

public enum FinishStatus {
    WITH_BORDER("FINISHED_WITH_BORDER"),
    WITH_ALL_DEAD("FINISHED_WITH_ALL_DEAD"),
    WITH_SAME_AS_PREVIOUS_STATE("FINISHED_WITH_SAME_AS_PREVIOUS_STATE"),
    WITH_MAX_EPOCHS("FINISHED_WITH_MAX_EPOCHS"),

    NOT_FINISHED("NOT_FINISHED");

    private final String status;

    FinishStatus(String status) {
        this.status = status;
    }

    public String getStatus() {
        return status;
    }
}

