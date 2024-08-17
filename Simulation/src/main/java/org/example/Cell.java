package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class Cell  {
    private boolean state; // true if alive, false if not


    public void setAlive() {
        state = true;
    }

    public void switchState() {
        state = !state;
    }

}
