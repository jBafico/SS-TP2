package org.example;

public record GridState<TStateMatrix>(TStateMatrix matrix, int aliveCells) {}
