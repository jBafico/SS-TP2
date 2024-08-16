package org.example;

import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.stream.IntStream;
import java.util.stream.Stream;

@Getter
@NoArgsConstructor
public class Grid2D extends GridAbstract<Cell[][]> {

    private Cell[][] matrix;
    private int m;
    private int r;
    private double initializationPercentage;
    private String radiusType;

    public Grid2D(int m, int r, double initializationPercentage, String radiousType) {
        matrix = new Cell[m][m];
        this.m = m;
        this.r = r;
        this.initializationPercentage = initializationPercentage;
        this.radiusType = radiousType;

        IntStream.range(0,m).forEach(i -> IntStream.range(0,m).forEach(j -> matrix[i][j] = new Cell()));
        switch (radiousType) {
            // case "VonNeumann" ->
            case "Moore" -> initializeWithMoore();
            default -> throw new RuntimeException("Invalid radius type");
        }
    }

    private void initializeWithMoore() {
        int middle = m / 2;
        for (int i = -r; i <= r; i++) {
            for (int j = -r; j <= r; j++) {
                int x = middle + i;
                int y = middle + j;
                if (x >= 0 && x < m && y >= 0 && y < m) { // border check
                    if (Math.random() <= initializationPercentage) {
                        matrix[x][y].setAlive();
                    }
                }
            }
        }
        System.out.println("");
    }

    @Override
    public Cell[][] cloneState() {

        Cell[][] matrixClone = new Cell[m][m];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                matrixClone[i][j] = this.matrix[i][j].cloneState();
            }
        }
        return matrixClone;
    }

    @Override
    public void evolve() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'evolve'");
    }

    @Override
    public boolean isFinished() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'isFinished'");
    }
}
