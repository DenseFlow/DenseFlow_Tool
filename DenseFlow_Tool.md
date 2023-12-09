# DenseFlow_Tool
## Introduction

This is a model used for money laundering detection on Ethereum based on the model DenseFlow. 

## Setting

In path Code/info.py change the path.

## Data

In path inputData/AML to see the data, stored according to case name, all-normal-addres.csv is the original transaction data.

## Run_model

Run main.ipynb

## Workflow

![image](https://github.com/DenseFlow/DenseFlow_Tool/blob/main/IMG/Fig_workflow.png)

## Symbols and Definitions  

| Symbols                   | Interpretation                                               |
| ------------------------- | ------------------------------------------------------------ |
| $G$                     | Downstream transaction network                               |
| $V$                       | Nodes of graph $G$                                           |
| $E$                       | Transaction edges of graph $G$, each edge $e=(i,j,a,t)$,sender's account ($i$), the recipient's account ($j$) |
| $a$                       | Transaction amount                                           |
| $t$                       | Transaction timestamp                                        |
| $e_{ji}$                  | Edge frequency from node $j$ to node $i$                     |
| $S$                       | Node subset of graph $G$                                     |
| $S^*$                     | Optimal subset                                               |
| $\alpha_i(S)$             | Topological suspiciousness of node $i$ within $S$            |
| $\beta_i(S)$              | Temporal suspiciousness of node $i$ within $S$               |
| $\gamma_i(S)$             | Monetary suspiciousness of node $i$ within $S$               |
| $\Phi\left[T_i(S)\right]$ | Timestamp set of transaction from $S$ to $v_i$               |
| $R$                       | Rating of transaction suspiciousness                         |
| $\omega_i$                | Weighted assigned to node $i$ in priority tree               |
| $F$                       | Accounts within suspicious money laundering flow             |
| $M$                       | Suspicious money laundering account set                      |
| $f_i(S)$                  | Suspicious function of node $i$ within $S$                   |
| $g(S)$                    | Suspicious function of subset $S$                            |
| $(t_o,a_o)$               | Awakening point of a surge in transactions calculated by the MultiBurst algorithm |
| $(t_p,a_p)$               | Peak point of a surge in transactions calculated by the MultiBurst algorithm |
| $\tau(t)$                 | Timestamp set of the transaction timestamp $t$ within the time slot |
| $A(\tau)$                 | Sum of the amounts for all transactions within the timestamp set $\tau$ |
| $\eta_i(S)$               | Sum of the numbers for all transactions in set $S$ with $i$  |
| $x_{ij}$                  | Flow on edge $(i,j)$ in Maximum Flow Algorithm               |



