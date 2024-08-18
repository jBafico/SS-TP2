package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class Cell  {
    private boolean alive; // true if alive, false if not


    public void setAlive() {
        alive = true;
    }

    public void switchState() {
        alive = !alive;
    }

}
