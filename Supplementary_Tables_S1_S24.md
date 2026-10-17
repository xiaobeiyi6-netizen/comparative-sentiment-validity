# Supplementary tables for the comparative validity audit

Primary outcomes use existing human labels and archived predictions. S11 reports VADER input perturbations; S19 separately reports executed RoBERTa input-protocol inference. All budget tables retain original-input predictions. Repeated splits and bootstrap samples reuse records and are not independent studies. No user accounts or individual predictions appear in these tables. Machine-readable CSV files retain full precision.


## Table S1 Airline All Budgets

Original airline protocol; seed 20261015, 200 repeats. MAE in pp; reversal rate is a fraction. Quantiles are conditional split percentiles. Human-only repeats across model rows refer to identical estimates.

| budget_per_airline | model | method | n_repetitions | mean_absolute_prevalence_error_pp_mean | mean_absolute_prevalence_error_pp_q025 | mean_absolute_prevalence_error_pp_q975 | reversal_rate_gap0pp_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 25 | roberta | ACC_airline_shrunk | 200 | 4.7441 | 1.9943 | 8.8347 | 0.0500 |
| 25 | roberta | ACC_pooled | 200 | 4.8609 | 2.2251 | 8.8532 | 0.0493 |
| 25 | roberta | CC | 200 | 3.7673 | 2.4961 | 4.9101 | 0.0493 |
| 25 | roberta | Human_calibration_only | 200 | 7.8242 | 3.6801 | 12.7137 | 0.1207 |
| 25 | vader | ACC_airline_shrunk | 200 | 15.8346 | 9.6150 | 25.2050 | 0.2843 |
| 25 | vader | ACC_pooled | 200 | 16.6209 | 9.8178 | 25.8167 | 0.2880 |
| 25 | vader | CC | 200 | 27.0907 | 25.1520 | 28.8972 | 0.2883 |
| 25 | vader | Human_calibration_only | 200 | 7.8242 | 3.6801 | 12.7137 | 0.1207 |
| 50 | roberta | ACC_airline_shrunk | 200 | 4.1501 | 2.0111 | 7.1243 | 0.0460 |
| 50 | roberta | ACC_pooled | 200 | 4.4084 | 2.4788 | 7.2887 | 0.0493 |
| 50 | roberta | CC | 200 | 3.7673 | 2.4961 | 4.9101 | 0.0493 |
| 50 | roberta | Human_calibration_only | 200 | 5.7213 | 3.0461 | 9.8867 | 0.0960 |
| 50 | vader | ACC_airline_shrunk | 200 | 14.0387 | 9.4926 | 21.5125 | 0.2763 |
| 50 | vader | ACC_pooled | 200 | 15.7244 | 10.5329 | 24.2660 | 0.2883 |
| 50 | vader | CC | 200 | 27.0907 | 25.1520 | 28.8972 | 0.2883 |
| 50 | vader | Human_calibration_only | 200 | 5.7213 | 3.0461 | 9.8867 | 0.0960 |
| 100 | roberta | ACC_airline_shrunk | 200 | 3.5175 | 1.9082 | 5.7592 | 0.0427 |
| 100 | roberta | ACC_pooled | 200 | 4.0173 | 2.5038 | 5.8303 | 0.0493 |
| 100 | roberta | CC | 200 | 3.7673 | 2.4961 | 4.9101 | 0.0493 |
| 100 | roberta | Human_calibration_only | 200 | 4.2336 | 2.0459 | 6.9715 | 0.0647 |
| 100 | vader | ACC_airline_shrunk | 200 | 11.9750 | 7.8740 | 18.2812 | 0.2540 |
| 100 | vader | ACC_pooled | 200 | 14.9955 | 9.7298 | 22.6656 | 0.2883 |
| 100 | vader | CC | 200 | 27.0907 | 25.1520 | 28.8972 | 0.2883 |
| 100 | vader | Human_calibration_only | 200 | 4.2336 | 2.0459 | 6.9715 | 0.0647 |
| 200 | roberta | ACC_airline_shrunk | 200 | 3.0537 | 1.5174 | 4.5562 | 0.0447 |
| 200 | roberta | ACC_pooled | 200 | 3.8350 | 2.3073 | 5.3252 | 0.0493 |
| 200 | roberta | CC | 200 | 3.7673 | 2.4961 | 4.9101 | 0.0493 |
| 200 | roberta | Human_calibration_only | 200 | 3.2275 | 1.5425 | 5.2348 | 0.0407 |
| 200 | vader | ACC_airline_shrunk | 200 | 9.8486 | 6.0232 | 14.8732 | 0.2070 |
| 200 | vader | ACC_pooled | 200 | 14.7000 | 10.4299 | 21.2567 | 0.2883 |
| 200 | vader | CC | 200 | 27.0907 | 25.1520 | 28.8972 | 0.2883 |
| 200 | vader | Human_calibration_only | 200 | 3.2275 | 1.5425 | 5.2348 | 0.0407 |
| 400 | roberta | ACC_airline_shrunk | 200 | 2.6107 | 1.1372 | 4.0654 | 0.0410 |
| 400 | roberta | ACC_pooled | 200 | 3.7479 | 2.3523 | 5.0986 | 0.0493 |
| 400 | roberta | CC | 200 | 3.7673 | 2.4961 | 4.9101 | 0.0493 |
| 400 | roberta | Human_calibration_only | 200 | 2.6610 | 1.0423 | 4.7494 | 0.0320 |
| 400 | vader | ACC_airline_shrunk | 200 | 7.7402 | 3.9580 | 12.0010 | 0.1370 |
| 400 | vader | ACC_pooled | 200 | 14.3958 | 10.0421 | 18.8827 | 0.2883 |
| 400 | vader | CC | 200 | 27.0907 | 25.1520 | 28.8972 | 0.2883 |
| 400 | vader | Human_calibration_only | 200 | 2.6610 | 1.0423 | 4.7494 | 0.0320 |


## Table S2 GOP All Budgets

Original GOP protocol; seed 20261016, 200 repeats. Reversal columns are fractions. All-pair denominator is 45; original >=10-pp set is fixed at 30 pairs. Full quantiles and additional metrics are in the CSV.

| budget_per_group | model | method | n_repetitions | mean_absolute_error_pp_mean | reversal_rate_all_mean | reversal_rate_fixed_gap10_mean | reversal_plus_half_ties_all_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 25 | RoBERTa | ACC_group_shrunk | 200 | 14.0076 | 0.2072 | 0.1412 | 0.2084 |
| 25 | RoBERTa | ACC_pooled | 200 | 14.4487 | 0.2094 | 0.1397 | 0.2132 |
| 25 | RoBERTa | CC | 200 | 16.3037 | 0.2102 | 0.1402 | 0.2127 |
| 25 | RoBERTa | Human_only | 200 | 9.3268 | 0.1668 | 0.0658 | 0.1979 |
| 25 | VADER | ACC_group_shrunk | 200 | 18.6778 | 0.2657 | 0.1905 | 0.2710 |
| 25 | VADER | ACC_pooled | 200 | 18.5416 | 0.2589 | 0.1818 | 0.2670 |
| 25 | VADER | CC | 200 | 25.2176 | 0.2634 | 0.1842 | 0.2668 |
| 25 | VADER | Human_only | 200 | 9.3268 | 0.1668 | 0.0658 | 0.1979 |
| 50 | RoBERTa | ACC_group_shrunk | 200 | 12.9852 | 0.2040 | 0.1380 | 0.2044 |
| 50 | RoBERTa | ACC_pooled | 200 | 13.8316 | 0.2097 | 0.1395 | 0.2126 |
| 50 | RoBERTa | CC | 200 | 16.3037 | 0.2102 | 0.1402 | 0.2127 |
| 50 | RoBERTa | Human_only | 200 | 7.6014 | 0.1558 | 0.0427 | 0.1724 |
| 50 | VADER | ACC_group_shrunk | 200 | 17.8161 | 0.2720 | 0.1967 | 0.2746 |
| 50 | VADER | ACC_pooled | 200 | 17.5051 | 0.2604 | 0.1822 | 0.2667 |
| 50 | VADER | CC | 200 | 25.2176 | 0.2634 | 0.1842 | 0.2668 |
| 50 | VADER | Human_only | 200 | 7.6014 | 0.1558 | 0.0427 | 0.1724 |
| 100 | RoBERTa | ACC_group_shrunk | 200 | 12.1610 | 0.2036 | 0.1343 | 0.2037 |
| 100 | RoBERTa | ACC_pooled | 200 | 13.5664 | 0.2098 | 0.1395 | 0.2126 |
| 100 | RoBERTa | CC | 200 | 16.3037 | 0.2102 | 0.1402 | 0.2127 |
| 100 | RoBERTa | Human_only | 200 | 6.4242 | 0.1304 | 0.0223 | 0.1384 |
| 100 | VADER | ACC_group_shrunk | 200 | 17.1108 | 0.2717 | 0.1975 | 0.2736 |
| 100 | VADER | ACC_pooled | 200 | 17.0799 | 0.2617 | 0.1835 | 0.2667 |
| 100 | VADER | CC | 200 | 25.2176 | 0.2634 | 0.1842 | 0.2668 |
| 100 | VADER | Human_only | 200 | 6.4242 | 0.1304 | 0.0223 | 0.1384 |


## Table S3 Group Confusion and Error

Exact original-input archived-prediction binary confusion counts. False-positive and false-negative contributions sum to signed prevalence bias. Rates and identity residuals are retained in the CSV.

| corpus | group | model | n | TP | FN | FP | TN | bias_pp | false_positive_component_pp | false_negative_component_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | American | VADER | 2759 | 992 | 968 | 73 | 726 | -32.4393 | 2.6459 | -35.0852 |
| Airline | American | RoBERTa | 2759 | 1751 | 209 | 151 | 648 | -2.1022 | 5.4730 | -7.5752 |
| Airline | Delta | VADER | 2222 | 489 | 466 | 120 | 1147 | -15.5716 | 5.4005 | -20.9721 |
| Airline | Delta | RoBERTa | 2222 | 766 | 189 | 115 | 1152 | -3.3303 | 5.1755 | -8.5059 |
| Airline | Southwest | VADER | 2420 | 589 | 597 | 96 | 1138 | -20.7025 | 3.9669 | -24.6694 |
| Airline | Southwest | RoBERTa | 2420 | 1002 | 184 | 137 | 1097 | -1.9421 | 5.6612 | -7.6033 |
| Airline | US Airways | VADER | 2913 | 1174 | 1089 | 82 | 568 | -34.5692 | 2.8150 | -37.3841 |
| Airline | US Airways | RoBERTa | 2913 | 1999 | 264 | 113 | 537 | -5.1837 | 3.8792 | -9.0628 |
| Airline | United | VADER | 3822 | 688 | 1945 | 27 | 1162 | -50.1832 | 0.7064 | -50.8896 |
| Airline | United | RoBERTa | 3822 | 2211 | 422 | 180 | 1009 | -6.3318 | 4.7096 | -11.0413 |
| Airline | Virgin America | VADER | 504 | 101 | 80 | 33 | 290 | -9.3254 | 6.5476 | -15.8730 |
| Airline | Virgin America | RoBERTa | 504 | 163 | 18 | 34 | 289 | 3.1746 | 6.7460 | -3.5714 |
| GOP | Ben Carson | VADER | 359 | 63 | 100 | 23 | 173 | -21.4485 | 6.4067 | -27.8552 |
| GOP | Ben Carson | RoBERTa | 359 | 91 | 72 | 31 | 165 | -11.4206 | 8.6351 | -20.0557 |
| GOP | Chris Christie | VADER | 181 | 48 | 66 | 11 | 56 | -30.3867 | 6.0773 | -36.4641 |
| GOP | Chris Christie | RoBERTa | 181 | 68 | 46 | 9 | 58 | -20.4420 | 4.9724 | -25.4144 |
| GOP | Donald Trump | VADER | 2047 | 559 | 800 | 130 | 558 | -32.7308 | 6.3508 | -39.0816 |
| GOP | Donald Trump | RoBERTa | 2047 | 823 | 536 | 180 | 508 | -17.3913 | 8.7934 | -26.1847 |
| GOP | Jeb Bush | VADER | 344 | 91 | 164 | 10 | 79 | -44.7674 | 2.9070 | -47.6744 |
| GOP | Jeb Bush | RoBERTa | 344 | 159 | 96 | 12 | 77 | -24.4186 | 3.4884 | -27.9070 |
| GOP | John Kasich | VADER | 222 | 22 | 50 | 17 | 133 | -14.8649 | 7.6577 | -22.5225 |
| GOP | John Kasich | RoBERTa | 222 | 34 | 38 | 12 | 138 | -11.7117 | 5.4054 | -17.1171 |
| GOP | Marco Rubio | VADER | 261 | 36 | 60 | 18 | 147 | -16.0920 | 6.8966 | -22.9885 |
| GOP | Marco Rubio | RoBERTa | 261 | 50 | 46 | 16 | 149 | -11.4943 | 6.1303 | -17.6245 |
| GOP | Mike Huckabee | VADER | 278 | 72 | 88 | 21 | 97 | -24.1007 | 7.5540 | -31.6547 |
| GOP | Mike Huckabee | RoBERTa | 278 | 108 | 52 | 23 | 95 | -10.4317 | 8.2734 | -18.7050 |
| GOP | Rand Paul | VADER | 240 | 58 | 71 | 15 | 96 | -23.3333 | 6.2500 | -29.5833 |
| GOP | Rand Paul | RoBERTa | 240 | 71 | 58 | 7 | 104 | -21.2500 | 2.9167 | -24.1667 |
| GOP | Scott Walker | VADER | 225 | 71 | 81 | 7 | 66 | -32.8889 | 3.1111 | -36.0000 |
| GOP | Scott Walker | RoBERTa | 225 | 80 | 72 | 4 | 69 | -30.2222 | 1.7778 | -32.0000 |
| GOP | Ted Cruz | VADER | 326 | 48 | 77 | 40 | 161 | -11.3497 | 12.2699 | -23.6196 |
| GOP | Ted Cruz | RoBERTa | 326 | 83 | 42 | 38 | 163 | -1.2270 | 11.6564 | -12.8834 |


## Table S4 Large Gap Reversals

All eight corpus-model-pair strict reversals with original reference gap >=10 pp. Every value is a difference in percentage points, with group_a minus group_b orientation.

| corpus | model | group_a | group_b | gold_diff_pp | pred_diff_pp | bias_difference_pp | fp_component_difference_pp | fn_component_difference_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | VADER | Delta | United | -25.9113 | 8.7003 | 34.6116 | 4.6941 | 29.9175 |
| Airline | VADER | Southwest | United | -19.8824 | 9.5983 | 29.4807 | 3.2605 | 26.2202 |
| Airline | VADER | United | Virgin America | 32.9779 | -7.8798 | -40.8578 | -5.8412 | -35.0166 |
| GOP | VADER | Chris Christie | Jeb Bush | -11.1445 | 3.2362 | 14.3807 | 3.1704 | 11.2103 |
| GOP | VADER | Jeb Bush | Mike Huckabee | 16.5740 | -4.0928 | -20.6667 | -4.6470 | -16.0197 |
| GOP | VADER | Jeb Bush | Rand Paul | 20.3779 | -1.0562 | -21.4341 | -3.3430 | -18.0911 |
| GOP | RoBERTa | Mike Huckabee | Scott Walker | -10.0016 | 9.7890 | 19.7906 | 6.4956 | 13.2950 |
| GOP | RoBERTa | Rand Paul | Ted Cruz | 15.4064 | -4.6166 | -20.0230 | -8.7398 | -11.2832 |


## Table S5 Reference and Duplicate Sensitivity

New revision sensitivity. Global normalized-text first occurrence defines the primary GOP archive. Modal sentiment ties retain the first occurring modal label. Model predictions are held fixed.

| variant | model | n | groups | pairs | reference_ties | predicted_ties | reversals | group_MAE_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline primary | VADER | 14640 | 6 | 15 | 0 | 0 | 3 | 27.1318 |
| Airline primary | RoBERTa | 14640 | 6 | 15 | 0 | 0 | 0 | 3.6775 |
| Airline confidence 1 | VADER | 10445 | 6 | 15 | 0 | 0 | 3 | 28.9359 |
| Airline confidence 1 | RoBERTa | 10445 | 6 | 15 | 0 | 0 | 0 | 2.5645 |
| GOP primary | VADER | 4483 | 10 | 45 | 0 | 0 | 7 | 25.1963 |
| GOP primary | RoBERTa | 4483 | 10 | 45 | 0 | 0 | 7 | 16.0009 |
| GOP majority labels | VADER | 4483 | 10 | 45 | 0 | 0 | 7 | 25.3735 |
| GOP majority labels | RoBERTa | 4483 | 10 | 45 | 0 | 0 | 7 | 16.1781 |
| GOP exclude cross-candidate texts | VADER | 4478 | 10 | 45 | 0 | 0 | 7 | 25.2283 |
| GOP exclude cross-candidate texts | RoBERTa | 4478 | 10 | 45 | 0 | 0 | 7 | 16.0169 |
| GOP repeated records | VADER | 6284 | 10 | 45 | 0 | 0 | 16 | 26.6758 |
| GOP repeated records | RoBERTa | 6284 | 10 | 45 | 0 | 0 | 5 | 17.4253 |


Repeated-record sensitivity maps the model prediction of each normalized text’s first retained occurrence back to eligible source records. Each record retains its own source human label and candidate. It evaluates record weighting under fixed canonical predictions, without rerunning inference on original text variants.

## Table S6 Shrinkage Grid

New revision sensitivity; paired original partitions at six k values. MAE in pp; reversal is a fraction. Native airline and GOP shrinkage implementations are retained separately. This is not out-of-sample parameter selection.

| corpus | budget | model | k | repetitions | MAE_pp | reversal_all | fallback_groups |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 25 | RoBERTa | 0 | 200 | 8.7139 | 0.1657 | 0.0000 |
| Airline | 25 | RoBERTa | 25 | 200 | 4.8647 | 0.0667 | 0.0000 |
| Airline | 25 | RoBERTa | 50 | 200 | 4.7272 | 0.0527 | 0.0000 |
| Airline | 25 | RoBERTa | 100 | 200 | 4.7441 | 0.0500 | 0.0000 |
| Airline | 25 | RoBERTa | 200 | 200 | 4.7817 | 0.0480 | 0.0000 |
| Airline | 25 | RoBERTa | 400 | 200 | 4.8150 | 0.0493 | 0.0000 |
| Airline | 25 | VADER | 0 | 200 | 19.9321 | 0.3010 | 0.4500 |
| Airline | 25 | VADER | 25 | 200 | 15.1521 | 0.2697 | 0.0000 |
| Airline | 25 | VADER | 50 | 200 | 15.4441 | 0.2803 | 0.0000 |
| Airline | 25 | VADER | 100 | 200 | 15.8346 | 0.2843 | 0.0000 |
| Airline | 25 | VADER | 200 | 200 | 16.1560 | 0.2847 | 0.0000 |
| Airline | 25 | VADER | 400 | 200 | 16.3673 | 0.2860 | 0.0000 |
| Airline | 50 | RoBERTa | 0 | 200 | 6.1793 | 0.1057 | 0.0000 |
| Airline | 50 | RoBERTa | 25 | 200 | 4.3291 | 0.0613 | 0.0000 |
| Airline | 50 | RoBERTa | 50 | 200 | 4.1502 | 0.0490 | 0.0000 |
| Airline | 50 | RoBERTa | 100 | 200 | 4.1501 | 0.0460 | 0.0000 |
| Airline | 50 | RoBERTa | 200 | 200 | 4.2295 | 0.0463 | 0.0000 |
| Airline | 50 | RoBERTa | 400 | 200 | 4.3020 | 0.0480 | 0.0000 |
| Airline | 50 | VADER | 0 | 200 | 14.6467 | 0.2283 | 0.1050 |
| Airline | 50 | VADER | 25 | 200 | 12.6247 | 0.2117 | 0.0000 |
| Airline | 50 | VADER | 50 | 200 | 13.2746 | 0.2627 | 0.0000 |
| Airline | 50 | VADER | 100 | 200 | 14.0387 | 0.2763 | 0.0000 |
| Airline | 50 | VADER | 200 | 200 | 14.6898 | 0.2857 | 0.0000 |
| Airline | 50 | VADER | 400 | 200 | 15.1528 | 0.2857 | 0.0000 |
| Airline | 100 | RoBERTa | 0 | 200 | 4.5058 | 0.0903 | 0.0000 |
| Airline | 100 | RoBERTa | 25 | 200 | 3.6846 | 0.0630 | 0.0000 |
| Airline | 100 | RoBERTa | 50 | 200 | 3.5158 | 0.0503 | 0.0000 |
| Airline | 100 | RoBERTa | 100 | 200 | 3.5175 | 0.0427 | 0.0000 |
| Airline | 100 | RoBERTa | 200 | 200 | 3.6399 | 0.0447 | 0.0000 |
| Airline | 100 | RoBERTa | 400 | 200 | 3.7786 | 0.0467 | 0.0000 |
| Airline | 100 | VADER | 0 | 200 | 10.5008 | 0.1743 | 0.0050 |
| Airline | 100 | VADER | 25 | 200 | 9.9041 | 0.1587 | 0.0000 |
| Airline | 100 | VADER | 50 | 200 | 10.8076 | 0.2097 | 0.0000 |
| Airline | 100 | VADER | 100 | 200 | 11.9750 | 0.2540 | 0.0000 |
| Airline | 100 | VADER | 200 | 200 | 13.0257 | 0.2770 | 0.0000 |
| Airline | 100 | VADER | 400 | 200 | 13.8321 | 0.2833 | 0.0000 |
| Airline | 200 | RoBERTa | 0 | 200 | 3.5002 | 0.0707 | 0.0000 |
| Airline | 200 | RoBERTa | 25 | 200 | 3.1337 | 0.0593 | 0.0000 |
| Airline | 200 | RoBERTa | 50 | 200 | 3.0402 | 0.0517 | 0.0000 |
| Airline | 200 | RoBERTa | 100 | 200 | 3.0537 | 0.0447 | 0.0000 |
| Airline | 200 | RoBERTa | 200 | 200 | 3.2059 | 0.0430 | 0.0000 |
| Airline | 200 | RoBERTa | 400 | 200 | 3.4091 | 0.0447 | 0.0000 |
| Airline | 200 | VADER | 0 | 200 | 8.0237 | 0.1420 | 0.0000 |
| Airline | 200 | VADER | 25 | 200 | 7.8507 | 0.1300 | 0.0000 |
| Airline | 200 | VADER | 50 | 200 | 8.5658 | 0.1530 | 0.0000 |
| Airline | 200 | VADER | 100 | 200 | 9.8486 | 0.2070 | 0.0000 |
| Airline | 200 | VADER | 200 | 200 | 11.2758 | 0.2557 | 0.0000 |
| Airline | 200 | VADER | 400 | 200 | 12.5319 | 0.2737 | 0.0000 |
| Airline | 400 | RoBERTa | 0 | 200 | 2.7566 | 0.0523 | 0.0000 |
| Airline | 400 | RoBERTa | 25 | 200 | 2.6365 | 0.0463 | 0.0000 |
| Airline | 400 | RoBERTa | 50 | 200 | 2.5946 | 0.0433 | 0.0000 |
| Airline | 400 | RoBERTa | 100 | 200 | 2.6107 | 0.0410 | 0.0000 |
| Airline | 400 | RoBERTa | 200 | 200 | 2.7540 | 0.0397 | 0.0000 |
| Airline | 400 | RoBERTa | 400 | 200 | 3.0030 | 0.0417 | 0.0000 |
| Airline | 400 | VADER | 0 | 200 | 6.5242 | 0.1137 | 0.0000 |
| Airline | 400 | VADER | 25 | 200 | 6.4731 | 0.1047 | 0.0000 |
| Airline | 400 | VADER | 50 | 200 | 6.7835 | 0.1130 | 0.0000 |
| Airline | 400 | VADER | 100 | 200 | 7.7402 | 0.1370 | 0.0000 |
| Airline | 400 | VADER | 200 | 200 | 9.1974 | 0.2007 | 0.0000 |
| Airline | 400 | VADER | 400 | 200 | 10.7880 | 0.2533 | 0.0000 |
| GOP | 25 | RoBERTa | 0 | 200 | 19.0667 | 0.2999 | 0.3400 |
| GOP | 25 | RoBERTa | 25 | 200 | 14.0388 | 0.2127 | 0.0000 |
| GOP | 25 | RoBERTa | 50 | 200 | 13.8821 | 0.2086 | 0.0000 |
| GOP | 25 | RoBERTa | 100 | 200 | 14.0076 | 0.2072 | 0.0000 |
| GOP | 25 | RoBERTa | 200 | 200 | 14.1729 | 0.2100 | 0.0000 |
| GOP | 25 | RoBERTa | 400 | 200 | 14.2975 | 0.2107 | 0.0000 |
| GOP | 25 | VADER | 0 | 200 | 25.3109 | 0.3586 | 1.8000 |
| GOP | 25 | VADER | 25 | 200 | 19.9822 | 0.2790 | 0.1150 |
| GOP | 25 | VADER | 50 | 200 | 19.0603 | 0.2667 | 0.0250 |
| GOP | 25 | VADER | 100 | 200 | 18.6778 | 0.2657 | 0.0100 |
| GOP | 25 | VADER | 200 | 200 | 18.5708 | 0.2633 | 0.0000 |
| GOP | 25 | VADER | 400 | 200 | 18.5409 | 0.2634 | 0.0000 |
| GOP | 50 | RoBERTa | 0 | 200 | 16.2524 | 0.2821 | 0.0400 |
| GOP | 50 | RoBERTa | 25 | 200 | 12.9832 | 0.2127 | 0.0000 |
| GOP | 50 | RoBERTa | 50 | 200 | 12.7998 | 0.2060 | 0.0000 |
| GOP | 50 | RoBERTa | 100 | 200 | 12.9852 | 0.2040 | 0.0000 |
| GOP | 50 | RoBERTa | 200 | 200 | 13.2871 | 0.2073 | 0.0000 |
| GOP | 50 | RoBERTa | 400 | 200 | 13.5163 | 0.2094 | 0.0000 |
| GOP | 50 | VADER | 0 | 200 | 23.6575 | 0.3483 | 0.9550 |
| GOP | 50 | VADER | 25 | 200 | 19.4285 | 0.2931 | 0.0650 |
| GOP | 50 | VADER | 50 | 200 | 18.4166 | 0.2817 | 0.0050 |
| GOP | 50 | VADER | 100 | 200 | 17.8161 | 0.2720 | 0.0000 |
| GOP | 50 | VADER | 200 | 200 | 17.5814 | 0.2676 | 0.0000 |
| GOP | 50 | VADER | 400 | 200 | 17.5066 | 0.2674 | 0.0000 |
| GOP | 100 | RoBERTa | 0 | 200 | 13.4690 | 0.2521 | 0.0050 |
| GOP | 100 | RoBERTa | 25 | 200 | 12.0896 | 0.2154 | 0.0000 |
| GOP | 100 | RoBERTa | 50 | 200 | 11.9561 | 0.2051 | 0.0000 |
| GOP | 100 | RoBERTa | 100 | 200 | 12.1610 | 0.2036 | 0.0000 |
| GOP | 100 | RoBERTa | 200 | 200 | 12.5727 | 0.2050 | 0.0000 |
| GOP | 100 | RoBERTa | 400 | 200 | 12.9636 | 0.2081 | 0.0000 |
| GOP | 100 | VADER | 0 | 200 | 20.7399 | 0.3336 | 0.3900 |
| GOP | 100 | VADER | 25 | 200 | 18.4747 | 0.2977 | 0.0300 |
| GOP | 100 | VADER | 50 | 200 | 17.6143 | 0.2818 | 0.0000 |
| GOP | 100 | VADER | 100 | 200 | 17.1108 | 0.2717 | 0.0000 |
| GOP | 100 | VADER | 200 | 200 | 16.9321 | 0.2666 | 0.0000 |
| GOP | 100 | VADER | 400 | 200 | 16.9385 | 0.2653 | 0.0000 |


## Table S7 Pairset and Tie Sensitivity

New revision sensitivity. Fixed10 uses original complete-archive pair gaps; holdout10 redefines eligibility using held-out human shares in each split. The latter denominator varies. No held-out labels fit the estimator. Counts and rates are means over 200 splits; rates are fractions.

| corpus | budget | model | method | k | reversal_all | reversal_fixed10 | reversal_holdout10 | holdout10_pairs | reference_ties | predicted_ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 25 | RoBERTa | CC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 25 | RoBERTa | Group ACC | 100 | 0.0500 | 0.0055 | 0.0022 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 25 | RoBERTa | Human-only | -1 | 0.1207 | 0.0380 | 0.0460 | 10.4650 | 0.0000 | 0.6700 |
| Airline | 25 | RoBERTa | Pooled ACC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 25 | VADER | CC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 25 | VADER | Group ACC | 100 | 0.2843 | 0.3255 | 0.3047 | 10.4650 | 0.0000 | 0.0400 |
| Airline | 25 | VADER | Human-only | -1 | 0.1207 | 0.0380 | 0.0460 | 10.4650 | 0.0000 | 0.6700 |
| Airline | 25 | VADER | Pooled ACC | -1 | 0.2880 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0550 |
| Airline | 50 | RoBERTa | CC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 50 | RoBERTa | Group ACC | 100 | 0.0460 | 0.0065 | 0.0017 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 50 | RoBERTa | Human-only | -1 | 0.0960 | 0.0135 | 0.0245 | 10.4650 | 0.0000 | 0.4000 |
| Airline | 50 | RoBERTa | Pooled ACC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 50 | VADER | CC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 50 | VADER | Group ACC | 100 | 0.2763 | 0.3135 | 0.2941 | 10.4650 | 0.0000 | 0.0250 |
| Airline | 50 | VADER | Human-only | -1 | 0.0960 | 0.0135 | 0.0245 | 10.4650 | 0.0000 | 0.4000 |
| Airline | 50 | VADER | Pooled ACC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0250 |
| Airline | 100 | RoBERTa | CC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 100 | RoBERTa | Group ACC | 100 | 0.0427 | 0.0070 | 0.0023 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 100 | RoBERTa | Human-only | -1 | 0.0647 | 0.0025 | 0.0084 | 10.4650 | 0.0000 | 0.2800 |
| Airline | 100 | RoBERTa | Pooled ACC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 100 | VADER | CC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 100 | VADER | Group ACC | 100 | 0.2540 | 0.2825 | 0.2661 | 10.4650 | 0.0000 | 0.0050 |
| Airline | 100 | VADER | Human-only | -1 | 0.0647 | 0.0025 | 0.0084 | 10.4650 | 0.0000 | 0.2800 |
| Airline | 100 | VADER | Pooled ACC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0100 |
| Airline | 200 | RoBERTa | CC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 200 | RoBERTa | Group ACC | 100 | 0.0447 | 0.0045 | 0.0019 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 200 | RoBERTa | Human-only | -1 | 0.0407 | 0.0005 | 0.0018 | 10.4650 | 0.0000 | 0.0750 |
| Airline | 200 | RoBERTa | Pooled ACC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 200 | VADER | CC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 200 | VADER | Group ACC | 100 | 0.2070 | 0.2060 | 0.1908 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 200 | VADER | Human-only | -1 | 0.0407 | 0.0005 | 0.0018 | 10.4650 | 0.0000 | 0.0750 |
| Airline | 200 | VADER | Pooled ACC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 400 | RoBERTa | CC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 400 | RoBERTa | Group ACC | 100 | 0.0410 | 0.0050 | 0.0010 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 400 | RoBERTa | Human-only | -1 | 0.0320 | 0.0005 | 0.0004 | 10.4650 | 0.0000 | 0.0300 |
| Airline | 400 | RoBERTa | Pooled ACC | -1 | 0.0493 | 0.0050 | 0.0014 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 400 | VADER | CC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 400 | VADER | Group ACC | 100 | 0.1370 | 0.1070 | 0.0988 | 10.4650 | 0.0000 | 0.0000 |
| Airline | 400 | VADER | Human-only | -1 | 0.0320 | 0.0005 | 0.0004 | 10.4650 | 0.0000 | 0.0300 |
| Airline | 400 | VADER | Pooled ACC | -1 | 0.2883 | 0.3305 | 0.3088 | 10.4650 | 0.0000 | 0.0000 |
| GOP | 25 | RoBERTa | CC | -1 | 0.2102 | 0.1402 | 0.1211 | 31.2150 | 0.1100 | 0.2250 |
| GOP | 25 | RoBERTa | Group ACC | 100 | 0.2072 | 0.1412 | 0.1198 | 31.2150 | 0.1100 | 0.1100 |
| GOP | 25 | RoBERTa | Human-only | -1 | 0.1668 | 0.0658 | 0.0988 | 31.2150 | 0.1100 | 2.8000 |
| GOP | 25 | RoBERTa | Pooled ACC | -1 | 0.2094 | 0.1397 | 0.1206 | 31.2150 | 0.1100 | 0.3350 |
| GOP | 25 | VADER | CC | -1 | 0.2634 | 0.1842 | 0.1817 | 31.2150 | 0.1100 | 0.3050 |
| GOP | 25 | VADER | Group ACC | 100 | 0.2657 | 0.1905 | 0.1855 | 31.2150 | 0.1100 | 0.4800 |
| GOP | 25 | VADER | Human-only | -1 | 0.1668 | 0.0658 | 0.0988 | 31.2150 | 0.1100 | 2.8000 |
| GOP | 25 | VADER | Pooled ACC | -1 | 0.2589 | 0.1818 | 0.1790 | 31.2150 | 0.1100 | 0.7300 |
| GOP | 50 | RoBERTa | CC | -1 | 0.2102 | 0.1402 | 0.1211 | 31.2150 | 0.1100 | 0.2250 |
| GOP | 50 | RoBERTa | Group ACC | 100 | 0.2040 | 0.1380 | 0.1154 | 31.2150 | 0.1100 | 0.0400 |
| GOP | 50 | RoBERTa | Human-only | -1 | 0.1558 | 0.0427 | 0.0762 | 31.2150 | 0.1100 | 1.4950 |
| GOP | 50 | RoBERTa | Pooled ACC | -1 | 0.2097 | 0.1395 | 0.1206 | 31.2150 | 0.1100 | 0.2600 |
| GOP | 50 | VADER | CC | -1 | 0.2634 | 0.1842 | 0.1817 | 31.2150 | 0.1100 | 0.3050 |
| GOP | 50 | VADER | Group ACC | 100 | 0.2720 | 0.1967 | 0.1958 | 31.2150 | 0.1100 | 0.2350 |
| GOP | 50 | VADER | Human-only | -1 | 0.1558 | 0.0427 | 0.0762 | 31.2150 | 0.1100 | 1.4950 |
| GOP | 50 | VADER | Pooled ACC | -1 | 0.2604 | 0.1822 | 0.1796 | 31.2150 | 0.1100 | 0.5650 |
| GOP | 100 | RoBERTa | CC | -1 | 0.2102 | 0.1402 | 0.1211 | 31.2150 | 0.1100 | 0.2250 |
| GOP | 100 | RoBERTa | Group ACC | 100 | 0.2036 | 0.1343 | 0.1136 | 31.2150 | 0.1100 | 0.0150 |
| GOP | 100 | RoBERTa | Human-only | -1 | 0.1304 | 0.0223 | 0.0455 | 31.2150 | 0.1100 | 0.7200 |
| GOP | 100 | RoBERTa | Pooled ACC | -1 | 0.2098 | 0.1395 | 0.1206 | 31.2150 | 0.1100 | 0.2500 |
| GOP | 100 | VADER | CC | -1 | 0.2634 | 0.1842 | 0.1817 | 31.2150 | 0.1100 | 0.3050 |
| GOP | 100 | VADER | Group ACC | 100 | 0.2717 | 0.1975 | 0.1948 | 31.2150 | 0.1100 | 0.1700 |
| GOP | 100 | VADER | Human-only | -1 | 0.1304 | 0.0223 | 0.0455 | 31.2150 | 0.1100 | 0.7200 |
| GOP | 100 | VADER | Pooled ACC | -1 | 0.2617 | 0.1835 | 0.1806 | 31.2150 | 0.1100 | 0.4500 |


## Table S8 Account Cluster Bootstrap

New revision sensitivity. 2,000 global paired recorded-account-name cluster bootstrap resamples, seed 20261016. Reversal columns are percentages; MAE columns are pp. Intervals are conditional empirical percentiles, not population-representative confidence intervals. Name strings are imperfect account identifiers.

| corpus | model | clusters | missing_accounts | repetitions | reversal_mean_pct | reversal_q025_pct | reversal_q975_pct | MAE_mean_pp | MAE_q025_pp | MAE_q975_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | RoBERTa | 7701 | 0 | 2000 | 3.3267 | 0.0000 | 13.3333 | 3.6841 | 2.9713 | 4.4045 |
| Airline | VADER | 7701 | 0 | 2000 | 26.0233 | 20.0000 | 40.0000 | 27.1055 | 25.9869 | 28.2852 |
| GOP | RoBERTa | 3287 | 0 | 2000 | 19.1067 | 11.1111 | 28.8889 | 16.1053 | 14.2065 | 18.0507 |
| GOP | VADER | 3287 | 0 | 2000 | 21.9044 | 11.1111 | 33.3333 | 25.2429 | 23.1007 | 27.4316 |


## Table S9 New fixed-revision inference comparison

| Corpus | Model | n | Binary changes | Archived reversals | New reversals |
|---|---|---:|---:|---:|---:|
| Airline | VADER | 14,640 | 0 | 3/15 | 3/15 |
| Airline | RoBERTa | 14,640 | 0 | 0/15 | 0/15 |
| GOP | VADER | 4,483 | 0 | 7/45 | 7/45 |
| GOP | RoBERTa | 4,483 | 0 | 7/45 | 7/45 |

Airline three-class changes were also zero. Historical GOP comparisons concern binary outcomes only. All group shares, MAEs and pair identities were unchanged, including original ≥3/5/10-pp sets. Fixed model revision: 3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7. This is a new run, not recovery of historical versions. Full-precision CSV: supplementary_tables/Table_S9_Locked_Inference_Comparison.csv.


# Reviewer revision of 17 October 2026

These retrospective analyses reuse released human labels and archived neural predictions. No new human annotation or transformer inference was conducted for S10–S18. Human-only rows repeated under both model names are computational bookkeeping, not independent observations. Full-precision CSV files accompany the readable selections below. All ranges are conditional archive variability.

## Table S10 Label allocation and sampling fractions

The table below shows the largest native budgets. The CSV contains every group at every tested native budget; holdouts use the native rounding rules.

| corpus | group | archive_n | evaluation_n | calibration_pool_n | budget | labeled_archive_pct | labeled_pool_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | American | 2759 | 552 | 2207 | 400 | 14.4980 | 18.1242 |
| Airline | Delta | 2222 | 445 | 1777 | 400 | 18.0018 | 22.5098 |
| Airline | Southwest | 2420 | 484 | 1936 | 400 | 16.5289 | 20.6612 |
| Airline | US Airways | 2913 | 583 | 2330 | 400 | 13.7315 | 17.1674 |
| Airline | United | 3822 | 765 | 3057 | 400 | 10.4657 | 13.0847 |
| Airline | Virgin America | 504 | 101 | 403 | 400 | 79.3651 | 99.2556 |
| GOP | Ben Carson | 359 | 72 | 287 | 100 | 27.8552 | 34.8432 |
| GOP | Chris Christie | 181 | 36 | 145 | 100 | 55.2486 | 68.9655 |
| GOP | Donald Trump | 2047 | 409 | 1638 | 100 | 4.8852 | 6.1050 |
| GOP | Jeb Bush | 344 | 69 | 275 | 100 | 29.0698 | 36.3636 |
| GOP | John Kasich | 222 | 44 | 178 | 100 | 45.0450 | 56.1798 |
| GOP | Marco Rubio | 261 | 52 | 209 | 100 | 38.3142 | 47.8469 |
| GOP | Mike Huckabee | 278 | 56 | 222 | 100 | 35.9712 | 45.0450 |
| GOP | Rand Paul | 240 | 48 | 192 | 100 | 41.6667 | 52.0833 |
| GOP | Scott Walker | 225 | 45 | 180 | 100 | 44.4444 | 55.5556 |
| GOP | Ted Cruz | 326 | 65 | 261 | 100 | 30.6748 | 38.3142 |

## Table S11 VADER input and lexicon perturbations

Original VADER 3.3.2 reproduces every archived binary airline prediction. The displayed rows are United; full CSV provides all six groups. All variants retain the original source labels, so this is a computational sensitivity, not newly annotated validation. The original lexicon score for united is +1.8.

| variant | n | predicted_pct | bias_pp | negative_recall_pct | recovered_original_false_negatives | archive_reversals |
| --- | --- | --- | --- | --- | --- | --- |
| Original input | 3822 | 18.7075 | -50.1832 | 26.1299 | 0 | 3 |
| All mention placeholders | 3822 | 37.9121 | -30.9785 | 50.5127 | 642 | 0 |
| URL placeholders | 3822 | 18.7075 | -50.1832 | 26.1299 | 0 | 3 |
| Model-card token placeholders | 3822 | 37.6504 | -31.2402 | 50.1329 | 632 | 0 |
| United handle only masked | 3822 | 37.9383 | -30.9524 | 50.5507 | 643 | 0 |
| Bare United only masked | 3822 | 19.5971 | -49.2936 | 27.3073 | 35 | 3 |
| United lexicon entry removed | 3822 | 38.8017 | -30.0890 | 51.6521 | 674 | 1 |

## Table S12 Forms of original United false negatives

All 3,822 United records contain the @United handle; consequently there is no observational within-United no-handle control group. Feature strata overlap, and their counts cannot establish a linguistic mechanism. No tweet text or account strings are distributed.

| feature | present | n | human_negatives | original_false_negatives | false_negative_rate_pct |
| --- | --- | --- | --- | --- | --- |
| United handle | True | 3822 | 2633 | 1945 | 73.8701 |
| United handle | False | 0 | 0 | 0 |  |
| Bare United | True | 216 | 162 | 142 | 87.6543 |
| Bare United | False | 3606 | 2471 | 1803 | 72.9664 |
| Any leading mention | True | 3728 | 2573 | 1900 | 73.8438 |
| Any leading mention | False | 94 | 60 | 45 | 75.0000 |
| URL | True | 243 | 143 | 112 | 78.3217 |
| URL | False | 3579 | 2490 | 1833 | 73.6145 |
| Retweet text prefix | True | 0 | 0 | 0 |  |
| Retweet text prefix | False | 3822 | 2633 | 1945 | 73.8701 |

## Table S13 Common implementation and formula comparison

Both corpora use seed 20261017, 200 repetitions, upward-rounded 20% message holdouts, nested budgets, shared fallback and tie handling. Both formulas run on identical samples. Shown: augmented-Jeffreys formula at 400 airline or 100 GOP labels; the CSV includes both formulas at all budgets. Changing only the formula alters group-ACC mean MAE by no more than 0.04 pp and strict reversal frequency by no more than 0.07 percentage points in this grid. Reference ties are excluded.

| corpus | budget | model | method | repetitions | MAE_pp_mean | strict_pct_mean | half_penalty_pct_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 400 | RoBERTa | CC | 200 | 3.7687 | 4.1667 | 4.1667 |
| Airline | 400 | RoBERTa | Group ACC | 200 | 2.5179 | 3.3667 | 3.3667 |
| Airline | 400 | RoBERTa | Human-only | 200 | 2.7017 | 3.2000 | 3.4000 |
| Airline | 400 | RoBERTa | Pooled ACC | 200 | 3.6943 | 4.1667 | 4.1667 |
| Airline | 400 | VADER | CC | 200 | 26.9803 | 28.4333 | 28.4333 |
| Airline | 400 | VADER | Group ACC | 200 | 8.0353 | 13.3333 | 13.3333 |
| Airline | 400 | VADER | Human-only | 200 | 2.7017 | 3.2000 | 3.4000 |
| Airline | 400 | VADER | Pooled ACC | 200 | 15.1218 | 28.4333 | 28.4333 |
| GOP | 100 | RoBERTa | CC | 200 | 16.1495 | 21.3205 | 21.4875 |
| GOP | 100 | RoBERTa | Group ACC | 200 | 12.1894 | 20.4439 | 20.4551 |
| GOP | 100 | RoBERTa | Human-only | 200 | 6.3320 | 12.7831 | 13.5225 |
| GOP | 100 | RoBERTa | Pooled ACC | 200 | 13.7079 | 21.3205 | 21.5042 |
| GOP | 100 | VADER | CC | 200 | 25.1188 | 26.4960 | 26.6462 |
| GOP | 100 | VADER | Group ACC | 200 | 18.2727 | 27.0321 | 27.2713 |
| GOP | 100 | VADER | Human-only | 200 | 6.3320 | 12.7831 | 13.5225 |
| GOP | 100 | VADER | Pooled ACC | 200 | 18.3519 | 26.2404 | 26.6241 |

## Table S14 Complete finite-archive target

Labels are sampled without a held-out subset. Known sampled labels enter the archive total exactly; machine estimates apply only to the unlabeled complement. Human-only is the random-sample label proportion. Raw CC uses zero labels and is shown as an available baseline under the budget cap. Augmented-Jeffreys rates, nested samples, 200 repetitions and seed 20261017 apply. The target is the complete archive reference, not future-message transfer. Displayed: largest feasible budgets; the CSV includes all budgets.

| corpus | budget | model | method | repetitions | MAE_pp_mean | strict_pct_mean | half_penalty_pct_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 400 | RoBERTa | Group ACC | 200 | 1.5582 | 0.4333 | 0.4333 |
| Airline | 400 | RoBERTa | Human-only | 200 | 1.5547 | 1.9000 | 2.0333 |
| Airline | 400 | RoBERTa | Label-assisted CC | 200 | 2.8361 | 0.0000 | 0.0000 |
| Airline | 400 | RoBERTa | Pooled ACC | 200 | 2.7431 | 0.1000 | 0.1000 |
| Airline | 400 | RoBERTa | Raw CC (no labels) | 200 | 3.6775 | 0.0000 | 0.0000 |
| Airline | 400 | VADER | Group ACC | 200 | 5.1832 | 3.4333 | 3.4333 |
| Airline | 400 | VADER | Human-only | 200 | 1.5547 | 1.9000 | 2.0333 |
| Airline | 400 | VADER | Label-assisted CC | 200 | 22.4406 | 33.2000 | 33.2000 |
| Airline | 400 | VADER | Pooled ACC | 200 | 10.9360 | 20.0667 | 20.0667 |
| Airline | 400 | VADER | Raw CC (no labels) | 200 | 27.1318 | 20.0000 | 20.0000 |
| GOP | 100 | RoBERTa | Group ACC | 200 | 5.8199 | 9.8333 | 9.8333 |
| GOP | 100 | RoBERTa | Human-only | 200 | 2.9979 | 5.0667 | 5.7222 |
| GOP | 100 | RoBERTa | Label-assisted CC | 200 | 10.2151 | 9.8667 | 9.8667 |
| GOP | 100 | RoBERTa | Pooled ACC | 200 | 7.3186 | 13.3111 | 13.3111 |
| GOP | 100 | RoBERTa | Raw CC (no labels) | 200 | 16.0009 | 15.5556 | 15.5556 |
| GOP | 100 | VADER | Group ACC | 200 | 7.5123 | 14.4889 | 14.4889 |
| GOP | 100 | VADER | Human-only | 200 | 2.9979 | 5.0667 | 5.7222 |
| GOP | 100 | VADER | Label-assisted CC | 200 | 16.5026 | 16.0889 | 16.0889 |
| GOP | 100 | VADER | Pooled ACC | 200 | 7.8890 | 14.7111 | 14.7111 |
| GOP | 100 | VADER | Raw CC (no labels) | 200 | 25.1963 | 15.5556 | 15.5556 |

## Table S15 Account-disjoint calibration and evaluation

Each repetition globally holds out all messages from 20% of recorded distinct account names. Calibration draws messages only from the other names. Budget 100 is displayed; 25 and 50 are in the CSV. Every one of the 200 repetitions per corpus supports every budget. Reference ties are excluded; names remain imperfect author identifiers and temporal/topic dependence is not removed.

| corpus | budget | model | method | repetitions | MAE_pp_mean | strict_pct_mean | half_penalty_pct_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 100 | RoBERTa | CC | 200 | 3.7930 | 5.0333 | 5.0333 |
| Airline | 100 | RoBERTa | Group ACC | 200 | 3.5127 | 4.6667 | 4.6667 |
| Airline | 100 | RoBERTa | Human-only | 200 | 4.7225 | 7.7333 | 8.3667 |
| Airline | 100 | RoBERTa | Pooled ACC | 200 | 4.0349 | 5.0333 | 5.0333 |
| Airline | 100 | VADER | CC | 200 | 27.2050 | 27.7000 | 27.7000 |
| Airline | 100 | VADER | Group ACC | 200 | 11.9042 | 25.3000 | 25.3000 |
| Airline | 100 | VADER | Human-only | 200 | 4.7225 | 7.7333 | 8.3667 |
| Airline | 100 | VADER | Pooled ACC | 200 | 14.9697 | 27.6667 | 27.7000 |
| GOP | 100 | RoBERTa | CC | 200 | 16.5716 | 21.0687 | 21.1577 |
| GOP | 100 | RoBERTa | Group ACC | 200 | 12.2956 | 20.3472 | 20.3750 |
| GOP | 100 | RoBERTa | Human-only | 200 | 7.0667 | 14.2937 | 15.1227 |
| GOP | 100 | RoBERTa | Pooled ACC | 200 | 13.5843 | 21.0242 | 21.1410 |
| GOP | 100 | VADER | CC | 200 | 25.5184 | 26.6045 | 26.6824 |
| GOP | 100 | VADER | Group ACC | 200 | 18.1052 | 26.9048 | 27.2283 |
| GOP | 100 | VADER | Human-only | 200 | 7.0667 | 14.2937 | 15.1227 |
| GOP | 100 | VADER | Pooled ACC | 200 | 17.9502 | 26.4154 | 26.7442 |

## Table S16 Native-protocol predicted ties

These reaggregate the original native partitions and retain their distinct denominators. Airline excludes reference ties (none in the 200 partitions); GOP retains 45 pairs and assigns reference ties zero strict inversions. Half penalty adds 0.5 for predicted ties where the reference is not tied. Largest budgets are displayed; all budgets are in the CSV.

| corpus | budget | model | method | repetitions | MAE_pp | strict_pct | predicted_ties | reference_ties | half_penalty_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 400 | RoBERTa | CC | 200 | 3.7673 | 4.9333 | 0.0000 | 0.0000 | 4.9333 |
| Airline | 400 | RoBERTa | Group ACC | 200 | 2.6107 | 4.1000 | 0.0000 | 0.0000 | 4.1000 |
| Airline | 400 | RoBERTa | Human-only | 200 | 2.6610 | 3.2000 | 0.0300 | 0.0000 | 3.3000 |
| Airline | 400 | RoBERTa | Pooled ACC | 200 | 3.7479 | 4.9333 | 0.0000 | 0.0000 | 4.9333 |
| Airline | 400 | VADER | CC | 200 | 27.0907 | 28.8333 | 0.0000 | 0.0000 | 28.8333 |
| Airline | 400 | VADER | Group ACC | 200 | 7.7402 | 13.7000 | 0.0000 | 0.0000 | 13.7000 |
| Airline | 400 | VADER | Human-only | 200 | 2.6610 | 3.2000 | 0.0300 | 0.0000 | 3.3000 |
| Airline | 400 | VADER | Pooled ACC | 200 | 14.3958 | 28.8333 | 0.0000 | 0.0000 | 28.8333 |
| GOP | 100 | RoBERTa | CC | 200 | 16.3037 | 21.0222 | 0.2250 | 0.1100 | 21.2722 |
| GOP | 100 | RoBERTa | Group ACC | 200 | 12.1610 | 20.3556 | 0.0150 | 0.1100 | 20.3722 |
| GOP | 100 | RoBERTa | Human-only | 200 | 6.4242 | 13.0444 | 0.7200 | 0.1100 | 13.8444 |
| GOP | 100 | RoBERTa | Pooled ACC | 200 | 13.5664 | 20.9778 | 0.2500 | 0.1100 | 21.2556 |
| GOP | 100 | VADER | CC | 200 | 25.2176 | 26.3444 | 0.3050 | 0.1100 | 26.6833 |
| GOP | 100 | VADER | Group ACC | 200 | 17.1108 | 27.1667 | 0.1700 | 0.1100 | 27.3556 |
| GOP | 100 | VADER | Human-only | 200 | 6.4242 | 13.0444 | 0.7200 | 0.1100 | 13.8444 |
| GOP | 100 | VADER | Pooled ACC | 200 | 17.0799 | 26.1667 | 0.4500 | 0.1100 | 26.6667 |

## Table S17 Repetition of text and source identifiers

A repeated identifier demonstrates that not all repeated CSV rows can be counted as distinct disseminated posts. Different identifiers on repeated wording still do not establish exposure or a complete release history.

| corpus | records | unique_normalized_texts | surplus_rows | repeated_text_groups | label_conflict_groups | cross_group_texts | repeated_tweet_id_groups | surplus_tweet_id_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline | 14640 | 14406 | 234 | 187 | 27 | 0 | 155 | 155 |
| GOP | 6284 | 4483 | 1801 | 150 | 60 | 5 | 19 | 19 |

Airline counterpart after first-occurrence normalized-text deduplication:

| variant | model | n | groups | pairs | reference_ties | predicted_ties | reversals | group_MAE_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airline unique normalized texts | VADER | 14406 | 6 | 15 | 0 | 0 | 3 | 27.3442 |
| Airline unique normalized texts | RoBERTa | 14406 | 6 | 15 | 0 | 0 | 0 | 3.7073 |

## Table S18 Fresh paired within-candidate bootstrap

5,000 within-candidate message resamples carry human and both model labels together (seed 20261017). Reference ordering is recomputed; reference ties are excluded. Percentiles are conditional ranges, not platform-population intervals. The difference row is calculated within each replicate before summarizing.

| model | repetitions | seed | MAE_pp_mean | MAE_pp_q025 | MAE_pp_q975 | strict_pct_mean | strict_pct_q025 | strict_pct_q975 | half_penalty_pct_mean | half_penalty_pct_q025 | half_penalty_pct_q975 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RoBERTa | 5000 | 20261017 | 16.1032 | 14.3703 | 17.8559 | 18.6586 | 11.1111 | 26.6667 | 18.6606 | 11.1111 | 26.6667 |
| VADER | 5000 | 20261017 | 25.2026 | 23.1562 | 27.2773 | 21.7063 | 11.1111 | 33.3333 | 21.7081 | 11.1111 | 33.3333 |
| VADER minus RoBERTa | 5000 | 20261017 | 9.0994 | 7.2769 | 10.9280 | 3.0478 | -8.8889 | 15.5556 | 3.0475 | -8.8889 | 15.5556 |

## Table S19 RoBERTa input-protocol sensitivity

Both conditions were actually inferred in one environment at model/tokenizer commit `3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7`, float32/eager, seed 20261017, original order, airline batch 32/no explicit max length, GOP batch 24/max length 128. Model-card preprocessing is the exact space-token algorithm from the pinned README; no other protocol element changes. Original-input binary labels match every archived primary label. Current runtime and assets are recorded in `audit/roberta_input/runtime.json`. This controlled run does not recover the historical environment. No budget results are recalculated with the placeholder outputs.

| corpus   | condition   |     n |   binary_changes |   binary_change_pct |   negative_pct |   binary_accuracy_pct |   group_MAE_pp |   gap0_reversals |   gap3_reversals |   gap5_reversals |   gap10_reversals |
|:---------|:------------|------:|-----------------:|--------------------:|---------------:|----------------------:|---------------:|-----------------:|-----------------:|-----------------:|------------------:|
| Airline  | original    | 14640 |             1140 |              7.7869 |        58.8934 |               86.2295 |         3.6775 |                0 |                0 |                0 |                 0 |
| Airline  | model_card  | 14640 |             1140 |              7.7869 |        51.2705 |               82.3907 |         9.9045 |                1 |                1 |                1 |                 0 |
| GOP      | original    |  4483 |              135 |              3.0114 |        42.3600 |               68.9940 |        16.0009 |                7 |                6 |                5 |                 2 |
| GOP      | model_card  |  4483 |              135 |              3.0114 |        42.7392 |               69.3286 |        15.2538 |                7 |                6 |                5 |                 2 |

Changes compare the two current input conditions, not different revisions. S19a gives overall results and threshold denominators; S19b gives both conditions for every group including TP/FN/FP/TN. S19c contains every unordered pair, with gap signs and preserved/disappeared/new labels. All pairs that reverse under either condition are listed below.

| corpus   | a              | b              |   reference_gap_pp |   original_gap_pp |   model_card_gap_pp | transition         |
|:---------|:---------------|:---------------|-------------------:|------------------:|--------------------:|:-------------------|
| Airline  | Delta          | Virgin America |             7.0666 |            0.5617 |             -0.1568 | new_reversal       |
| GOP      | Ben Carson     | Rand Paul      |            -8.3461 |            1.4833 |              1.0689 | preserved_reversal |
| GOP      | Ben Carson     | Ted Cruz       |             7.0603 |           -3.1333 |             -2.9111 | preserved_reversal |
| GOP      | Chris Christie | Mike Huckabee  |             5.4295 |           -4.5809 |             -4.0284 | preserved_reversal |
| GOP      | Chris Christie | Scott Walker   |            -4.5721 |            5.2081 |              2.6495 | preserved_reversal |
| GOP      | Donald Trump   | Scott Walker   |            -1.1657 |           11.6652 |              8.4075 | preserved_reversal |
| GOP      | Mike Huckabee  | Scott Walker   |           -10.0016 |            9.7890 |              6.6779 | preserved_reversal |
| GOP      | Rand Paul      | Ted Cruz       |            15.4064 |           -4.6166 |             -3.9801 | preserved_reversal |

## Table S20 Token lengths and actual truncation

Untruncated lengths include both special tokens. The airline tokenizer’s very large sentinel disables automatic truncation; it is not an operative length cap. The model architecture supports 512 total tokens, and observed inputs remain below capacity. GOP truncates only inputs longer than its explicit 128-token maximum. Group-level counts and maxima are in the full CSV.

| corpus   | condition   |     n |   max_tokens_with_specials |   over128 |   over128_pct |   actual_truncated |   actual_truncated_pct |   architecture_capacity |
|:---------|:------------|------:|---------------------------:|----------:|--------------:|-------------------:|-----------------------:|------------------------:|
| Airline  | original    | 14640 |                        132 |         1 |        0.0068 |                  0 |                 0.0000 |                     512 |
| Airline  | model_card  | 14640 |                        130 |         1 |        0.0068 |                  0 |                 0.0000 |                     512 |
| GOP      | original    |  4483 |                        123 |         0 |        0.0000 |                  0 |                 0.0000 |                     512 |
| GOP      | model_card  |  4483 |                        123 |         0 |        0.0000 |                  0 |                 0.0000 |                     512 |

## Table S21 Paired Group ACC versus human-only differences

Difference is Group ACC minus human-only: a negative loss difference favors Group ACC. Each cell has 200 independent protocol draws conditional on the fixed archive. Monte Carlo SE is the paired-difference sample SD divided by √200; it describes simulation-mean precision, not population uncertainty. Conditional split quantiles describe variability rather than this precision. Better/same/worse uses absolute tolerance 1e-12; native GOP retains its fixed comparison denominator.

| mode            | metric           |   mean_difference |   Monte_Carlo_SE |   group_better |   same |   group_worse |
|:----------------|:-----------------|------------------:|-----------------:|---------------:|-------:|--------------:|
| finite_archive  | MAE_pp           |            0.0034 |           0.0483 |             99 |      0 |           101 |
| finite_archive  | strict_pct       |           -1.4667 |           0.2463 |             52 |    139 |             9 |
| finite_archive  | half_penalty_pct |           -1.6000 |           0.2467 |             60 |    131 |             9 |
| message_holdout | MAE_pp           |           -0.1838 |           0.0840 |            105 |      0 |            95 |
| message_holdout | strict_pct       |            0.1667 |           0.4212 |             51 |     97 |            52 |
| message_holdout | half_penalty_pct |           -0.0333 |           0.4279 |             55 |     93 |            52 |
| native          | MAE_pp           |           -0.0503 |           0.0839 |            106 |      0 |            94 |
| native          | strict_pct       |            0.9000 |           0.4623 |             44 |    100 |            56 |
| native          | half_penalty_pct |            0.8000 |           0.4602 |             47 |     97 |            56 |

Full CSV includes every corpus, budget, classifier, native/common formula, finite-archive and account-disjoint design.

## Table S22 ACC operating diagnostics

The diagnostic rerun reproduces every stored common-design score. Existing fallback counts are retained. For each corpus/design/budget/model/formula/estimator cell, the full table reports 200 repetitions and total group-repetitions. Each event has both mean affected groups per repetition and percent of group-repetitions. Only applied, nonfallback corrections contribute lower/upper pre-clipping excursions. Negative denominators count all groups, including fallback; there are none in these runs. Clipping-created ties concern reference-non-tied pairs, with finite-archive estimates recombined before checking ties. Per-repeat records are in `audit/round2/acc_diagnostics_replicates.csv`.

| corpus   | mode            |   budget | model   | rule               | method     |   fallback_groups_mean_per_repeat |   fallback_groups_pct_group_repetitions |   preclip_below0_groups_pct_group_repetitions |   preclip_above1_groups_pct_group_repetitions |
|:---------|:----------------|---------:|:--------|:-------------------|:-----------|----------------------------------:|----------------------------------------:|----------------------------------------------:|----------------------------------------------:|
| GOP      | account_holdout |       25 | VADER   | augmented_Jeffreys | Group ACC  |                            0.0400 |                                  0.4000 |                                        7.4500 |                                        7.2500 |
| GOP      | account_holdout |       25 | VADER   | augmented_Jeffreys | Pooled ACC |                            0.0000 |                                  0.0000 |                                        7.1500 |                                        7.0500 |
| GOP      | account_holdout |       50 | VADER   | augmented_Jeffreys | Group ACC  |                            0.0050 |                                  0.0500 |                                        5.7000 |                                        6.5000 |
| GOP      | finite_archive  |       25 | VADER   | augmented_Jeffreys | Group ACC  |                            0.0400 |                                  0.4000 |                                        1.4500 |                                        2.8500 |
| GOP      | finite_archive  |       25 | VADER   | augmented_Jeffreys | Pooled ACC |                            0.0500 |                                  0.5000 |                                        1.5000 |                                        3.0000 |
| GOP      | message_holdout |       25 | VADER   | augmented_Jeffreys | Group ACC  |                            0.0100 |                                  0.1000 |                                        5.9000 |                                        6.5000 |
| GOP      | message_holdout |       25 | VADER   | blend_Jeffreys     | Group ACC  |                            0.0050 |                                  0.0500 |                                        6.0000 |                                        6.5000 |

## Table S23 Duplicate-label conflict scale

Conflicting groups are groups of repeated normalized text, not known annotation errors. Associated-record counts include all records in each conflicted group, not only surplus rows. The binary task merges neutral and positive, so its conflict count can be smaller. Neither 60/150 nor any associated-record ratio estimates the corpus label-error rate.

| corpus   |   eligible_records |   unique_normalized_texts |   repeated_text_groups |   records_in_repeated_groups |   threeclass_conflict_groups |   records_in_threeclass_conflict_groups |   binary_conflict_groups |   records_in_binary_conflict_groups |
|:---------|-------------------:|--------------------------:|-----------------------:|-----------------------------:|-----------------------------:|----------------------------------------:|-------------------------:|------------------------------------:|
| Airline  |              14640 |                     14406 |                    187 |                          421 |                           27 |                                      73 |                        8 |                                  16 |
| GOP      |               6284 |                      4483 |                    150 |                         1951 |                           60 |                                    1539 |                       56 |                                1435 |

## Table S24 Supervised-text overlap in both primary archives

Both corpora are screened using identical HTML unescaping, NFKC, case folding and whitespace collapse against the same hash-identified TweetEval sentiment training and validation text files. Matching is exact after normalization; the counts do not establish approximate-match or pretraining independence. Input hashes, URLs, line counts and unique text counts are in `audit/round2/overlap_sources.json`; the full CSV includes group counts.

| corpus   | supervised_split   | group   |     n |   matching_records |   matching_unique_normalized_texts |
|:---------|:-------------------|:--------|------:|-------------------:|-----------------------------------:|
| Airline  | train              | ALL     | 14640 |                  0 |                                  0 |
| GOP      | train              | ALL     |  4483 |                  1 |                                  1 |
| Airline  | val                | ALL     | 14640 |                  0 |                                  0 |
| GOP      | val                | ALL     |  4483 |                  0 |                                  0 |
