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




## Empirical evidence on the density issue

Here we provide some empirical evidence on the density issue of money laundering networks from reports of blockchain security companies.

### Figure 1. Cylynx: Money Laundering Illustration of UpbitHack Case [1] ###
![image](https://github.com/DenseFlow/DenseFlow_Tool/blob/main/IMG/Fig_UpbitHack.png)

[1] Cylynx. 2020. Tracing the Trail of the Upbit Hack. https://www.cylynx.io/blog/tracing-the-trail-of-the-upbit-hack/


### Figure 2. Peckshield: Money Laundering Illustration of PlusTokenPonzi Case [2][3] ###

![image](https://github.com/DenseFlow/DenseFlow_Tool/blob/main/IMG/Fig_PlusTokenPonzi.jpg)


[2] PeckShield Team. 2021. Digital currency anti-money laundering research report: 2020 annual report. https://coinholmes.com/static/pdf/2020_2.pdf

[3] PeckShield Team. PlusToken new bottles of old wine cheat 10 billion OTC into an important access to gold channel. https://mp.weixin.qq.com/s/y5R3Raznu3dVMDFsAz25ww


### Figure 3. TRM Lab: Money Laundering Illustration of Pig Butchering Scams [4] ###

![image](https://github.com/DenseFlow/DenseFlow_Tool/blob/main/IMG/Fig_Pig_Butchering.png)

[4] TRM Lab. 2023. Illicit crypto ecosystem report: A comprehensive guide to illicit finance risks in crypto. https://www.trmlabs.com/report#Fraud-and-Scams


### Figure 4. Elliptic: Money Laundering Network Illustration of Cryptocurrency Crimes [5] ###
![image](https://github.com/DenseFlow/DenseFlow_Tool/blob/main/IMG/Fig_Elliptic.png)

[5] Elliptic Team. 2023. The state of cross-chain crime. https://www.elliptic.co/resources/state-of-cross-chain-crime-2023#:~:text=The%20State%20of%20Cross-chain%20Crime%202023%20In%20October,decentralized%20exchanges%2C%20cross-chain%20bridges%20and%20coin%20swap%20services.



