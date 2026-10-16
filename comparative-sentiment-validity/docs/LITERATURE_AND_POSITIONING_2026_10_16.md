# Verified related research (additional to the manuscript's earlier 12 items)

This is a **targeted update**, not a systematic literature review or evidence of an exhaustive Web of Science search. Entries were checked against publisher or ACL Anthology pages on 16 October 2026.

## Birkenmaier, Lechner, and Wagner (2024)

Birkenmaier, L., Lechner, C. M., & Wagner, C. (2024). The search for solid ground in text as data: A systematic review of validation practices and practical recommendations for validation. Communication Methods and Measures, 18(3), 249–277. https://doi.org/10.1080/19312458.2023.2285765

- Confirmed source: https://www.tandfonline.com/doi/full/10.1080/19312458.2023.2285765
- How the manuscript must address it: directly addresses construct validation practices in computational communication; our novelty is post-classification object ranking, not validation generally.

## TeBlunthuis, Hase, and Chan (2024)

TeBlunthuis, N., Hase, V., & Chan, C.-H. (2024). Misclassification in automated content analysis causes bias in regression. Can we fix it? Yes we can! Communication Methods and Measures, 18(3), 278–299. https://doi.org/10.1080/19312458.2023.2293713

- Confirmed source: https://www.tandfonline.com/doi/abs/10.1080/19312458.2023.2293713
- How the manuscript must address it: direct competitor in downstream error correction; their focal issue is regression bias, whereas the present paper audits pairwise descriptive rank reversals and human-label budgets.

## Mu, Jin, Song, and Aletras (2024)

Mu, Y., Jin, M., Song, X., & Aletras, N. (2024). Enhancing data quality through simple de-duplication: Navigating responsible computational social science research. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (pp. 12477–12492). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.emnlp-main.694

- Confirmed source: https://aclanthology.org/2024.emnlp-main.694/
- How the manuscript must address it: direct relevance to deduplication and leakage; this paper treats unique text versus repeated records as alternative estimands, not unilaterally improved accuracy.

## Hou and Huang (2025)

Hou, Y., & Huang, J. (2025). Natural language processing for social science research: A comprehensive review. Chinese Journal of Sociology, 11(1). https://doi.org/10.1177/2057150X241306780

- Confirmed source: https://journals.sagepub.com/doi/10.1177/2057150X241306780
- How the manuscript must address it: background review on representativeness, interpretability and bias; broad context not direct prior rank-reversal study.

## Hase, Bachl, and TeBlunthuis (2025)

Hase, V., Bachl, M., & TeBlunthuis, N. (2025). Critical, but constructive: Defining, detecting, and addressing bias in computational social science. Communication Methods and Measures, 19(4), 281–293. https://doi.org/10.1080/19312458.2025.2575468

- Confirmed source: https://www.tandfonline.com/doi/full/10.1080/19312458.2025.2575468
- How the manuscript must address it: framework context on defining/detecting/addressing bias; supports method-level contribution but no claim of novelty of bias correction.

## Novelty boundary

- **Already established:** classification errors produce aggregate prevalence bias, class-quantification methods can outperform classify-and-count, and automated content analyses can bias downstream regression. Do not claim priority for those insights.
- **Supported incremental study contribution:** strict pairwise object-ranking reversals, reference-gap-conditioned comparison, observed between-group FPR/FNR decomposition, differences between distinct-text and repeated-record estimands, and same-budget contrasts of ACC versus direct human-only estimates in two real archives.
- **Unresolved:** no population sampling, no causal platform algorithm inference, no original RoBERTa commit, and no completed public data-release license review. A descriptive study may remain publishable, but novelty is not proven solely by these additions.

## Priority revisions

1. Explicitly cite TeBlunthuis et al. (2024) and Birkenmaier et al. (2024) when framing the contribution.
2. Cite Mu et al. (2024) when discussing unique-text versus repeated-message estimands.
3. Use Hase et al. (2025) to position bias as a measurement problem in CSS, not as an invented new observation.
4. Explain that human-only direct estimates often beat sophisticated calibration under the GOP label budgets tested.
5. Keep the 2025 NLP review as broad context only, if space permits.
