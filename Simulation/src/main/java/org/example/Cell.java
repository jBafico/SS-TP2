package org.example;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@NoArgsConstructor
public class Cell  {
    private boolean state = false; // true if alive, false if not


    public void setAlive() {
        state = true;
    }

    public void switchState() {
        state = !state;
    }

    public Cell cloneState() {
        return new Cell(this.state);
    }
}
