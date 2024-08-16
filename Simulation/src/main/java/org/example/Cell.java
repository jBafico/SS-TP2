package org.example;

public class Cell {
    private int state; //El estado puede ser 0 o 1

    public Cell(int state) {
        this.state = state;
    }

    public int getState() {
        return state;
    }

    public void switchState() {
        switch (state) {
            case 0:
                state = 1;
                break;
            case 1:
                state = 0;
                break;
        }
    }
}
