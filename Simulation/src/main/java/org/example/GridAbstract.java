package org.example;

public abstract class GridAbstract<TMatrix> {
    

    public abstract TMatrix cloneState();
    public abstract void evolve();
    public abstract boolean isFinished();
}
