# Judge calibration sheet (v2, validation claims)

Label every item in `labels_v2.csv` using JUDGE_RUBRIC.md. Use only the abstracts shown here, not your own knowledge.

## v2-01 — faithfulness

**Claim:** Lamins are associated with nuclear membrane structure maintenance.

**Answer sentences:**

1. Lamins are associated with nuclear membrane structure maintenance, as evidenced by the role of lamin A in the nuclear structural defects observed in Hutchinson-Gilford progeria syndrome [34747208].
2. Additionally, lamin B1 is involved in maintaining chromatin condensation and genome integrity, which are essential for proper nuclear structure [25036988].
3. The interaction of LC3 with lamin B1 further highlights the importance of lamins in nuclear lamina organization [4452659].
4. These findings collectively support the role of lamins in nuclear membrane structure maintenance.

**Cited abstracts:**

> **[34747208] Lamin A-dependent nuclear defects in human aging.**
>
> Mutations in the nuclear structural protein lamin A cause the premature aging syndrome Hutchinson-Gilford progeria (HGPS). Whether lamin A plays any role in normal aging is unknown. We show that the same molecular mechanism responsible for HGPS is active in healthy cells. Cell nuclei from old individuals acquire defects similar to those of HGPS patient cells, including changes in histone modifications and increased DNA damage. Age-related nuclear defects are caused by sporadic use, in healthy individuals, of the same cryptic splice site in lamin A whose constitutive activation causes HGPS. Inhibition of this splice site reverses the nuclear defects associated with aging. These observations implicate lamin A in physiological aging.

> **[25036988] Loss of lamin B1 results in prolongation of S phase and decondensation of chromosome territories.**
>
> Nuclear lamin B1 (LMNB1) constitutes one of the major structural proteins in the lamina mesh. We silenced the expression of LMNB1 by RNA interference in the colon cancer cell line DLD-1 and showed a dramatic redistribution of H3K27me3 from the periphery to a more homogeneous nuclear dispersion. In addition, we observed telomere attrition and an increased frequency of micronuclei and nuclear blebs. By 3D-FISH analyses, we demonstrated that the volume and surface of chromosome territories were significantly larger in LMNB1-depleted cells, suggesting that LMNB1 is required to maintain chromatin condensation in interphase nuclei. These changes led to a prolonged S phase due to activation of Chk1. Finally, silencing of LMNB1 resulted in extensive changes in alternative splicing of multiple genes and in a higher number of enlarged nuclear speckles. Taken together, our results suggest a mechanistic role of the nuclear lamina in the organization of chromosome territories, maintenance of genome integrity and proper gene splicing.

> **[4452659] Autophagy mediates degradation of nuclear lamina**
>
> Macroautophagy (hereafter referred to as autophagy) is a catabolic membrane trafficking process that degrades a variety of cellular constituents and is associated with human diseases. Although extensive studies have focused on autophagic turnover of cytoplasmic materials, little is known about the role of autophagy in degrading nuclear components. Here we report that the autophagy machinery mediates degradation of nuclear lamina components in mammals. The autophagy protein LC3/Atg8, which is involved in autophagy membrane trafficking and substrate delivery, is present in the nucleus and directly interacts with the nuclear lamina protein lamin B1, and binds to lamin-associated domains on chromatin. This LC3-lamin B1 interaction does not downregulate lamin B1 during starvation, but mediates its degradation upon oncogenic insults, such as by activated RAS. Lamin B1 degradation is achieved by nucleus-to-cytoplasm transport that delivers lamin B1 to the lysosome. Inhibiting autophagy or the LC3-lamin B1 interaction prevents activated RAS-induced lamin B1 loss and attenuates oncogene-induced senescence in primary human cells. Our study suggests that this new function of autophagy acts as a guarding mechanism protecting cells from tumorigenesis.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-02 — faithfulness

**Claim:** Deleting Raptor increases G-CSF levels.

**Answer sentences:**

1. The provided abstracts do not mention any relationship between deleting Raptor and G-CSF levels. [2014909] discusses the role of mTOR signaling in regulating G-CSF but does not address the effect of Raptor deletion on G-CSF levels. [22174015] mentions Raptor but does not discuss G-CSF.
2. Therefore, the claim is not supported by the given abstracts.

**Cited abstracts:**

> **[2014909] Oncogenic mTOR signaling recruits myeloid-derived suppressor cells to promote tumor initiation**
>
> Myeloid-derived suppressor cells (MDSCs) play critical roles in primary and metastatic cancer progression. MDSC regulation is widely variable even among patients harbouring the same type of malignancy, and the mechanisms governing such heterogeneity are largely unknown. Here, integrating human tumour genomics and syngeneic mammary tumour models, we demonstrate that mTOR signalling in cancer cells dictates a mammary tumour's ability to stimulate MDSC accumulation through regulating G-CSF. Inhibiting this pathway or its activators (for example, FGFR) impairs tumour progression, which is partially rescued by restoring MDSCs or G-CSF. Tumour-initiating cells (TICs) exhibit elevated G-CSF. MDSCs reciprocally increase TIC frequency through activating Notch in tumour cells, forming a feedforward loop. Analyses of primary breast cancers and patient-derived xenografts corroborate these mechanisms in patients. These findings establish a non-canonical oncogenic role of mTOR signalling in recruiting pro-tumorigenic MDSCs and show how defined cancer subsets may evolve to promote and depend on a distinct immune microenvironment.

> **[22174015] PI3K-Akt-mTORC1-S6K1/2 axis controls Th17 differentiation by regulating Gfi1 expression and nuclear translocation of RORγ.**
>
> The PI3K-Akt-mTORC1 axis contributes to the activation, survival, and proliferation of CD4(+) T cells upon stimulation through TCR and CD28. Here, we demonstrate that the suppression of this axis by deletion of p85α or PI3K/mTORC1 inhibitors as well as T cell-specific deletion of raptor, an essential component of mTORC1, impairs Th17 differentiation in vitro and in vivo in a S6K1/2-dependent fashion. Inhibition of PI3K-Akt-mTORC1-S6K1 axis impairs the downregulation of Gfi1, a negative regulator of Th17 differentiation. Furthermore, we demonstrate that S6K2, a nuclear counterpart of S6K1, is induced by the PI3K-Akt-mTORC1 axis, binds RORγ, and carries RORγ to the nucleus. These results point toward a pivotal role of PI3K-Akt-mTORC1-S6K1/2 axis in Th17 differentiation.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-03 — abstention

**Claim:** Mice defective for deoxyribonucleic acid (DNA) polymerase I (polI) fail to reveal increased sensitivity to ionizing radiation (IR).

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[11569583] Deregulated DNA polymerase β strengthens ionizing radiation-induced nucleotidic and chromosomal instabilities**
>
> DNA polymerase β (Pol β) is an error-prone enzyme which has been found to be overexpressed in several human tumors. By using a couple of recombinant CHO cells differing only from the exogenous expression of Pol β, we showed here that cells overexpressing Pol β are much more sensitive to IR treatments by increasing apoptosis. We also found that the surviving cells displayed an hypermutator phenotype which could be explained by different pathways involving Pol β, such as (i) an increased capacity to incorporate into DNA the mutagenic dGTP analog, 8-oxo-dGTP, one of the most abundant purine-derived nucleotides exposed to γ-irradiation, (ii) the induction of IR-induced DNA breaks and (iii) accumulation of chromosome aberrations induced by radiation. Alteration of Pol β expression in irradiated cells thus appears to strengthen both cell death and genetic changes associated with a malignant phenotype. These data provide new insights into the cellular response to radiations and the associated carcinogenic consequences.

> **[27635177] Association of DNA polymerase mu (pol mu) with Ku and ligase IV: role for pol mu in end-joining double-strand break repair.**
>
> Mammalian DNA polymerase mu (pol mu) is related to terminal deoxynucleotidyl transferase, but its biological role is not yet clear. We show here that after exposure of cells to ionizing radiation (IR), levels of pol mu protein increase. pol mu also forms discrete nuclear foci after IR, and these foci are largely coincident with IR-induced foci of gammaH2AX, a previously characterized marker of sites of DNA double-strand breaks. pol mu is thus part of the cellular response to DNA double-strand breaks. pol mu also associates in cell extracts with the nonhomologous end-joining repair factor Ku and requires both Ku and another end-joining factor, XRCC4-ligase IV, to form a stable complex on DNA in vitro. pol mu in turn facilitates both stable recruitment of XRCC4-ligase IV to Ku-bound DNA and ligase IV-dependent end joining. In contrast, the related mammalian DNA polymerase beta does not form a complex with Ku and XRCC4-ligase IV and is less effective than pol mu in facilitating joining mediated by these factors. Our data thus support an important role for pol mu in the end-joining pathway for repair of double-strand breaks.

> **[31293581] Ionizing radiation-induced long-term expression of senescence markers in mice is independent of p53 and immune status.**
>
> Exposure to IR has been shown to induce the formation of senescence markers, a phenotype that coincides with lifelong delayed repair and regeneration of irradiated tissues. We hypothesized that IR-induced senescence markers could persist long-term in vivo, possibly contributing to the permanent reduction in tissue functionality. Here, we show that mouse tissues exposed to a sublethal dose of IR display persistent (up to 45 weeks, the maximum time analyzed) DNA damage foci and increased p16(INK4a) expression, two hallmarks of cellular senescence and aging. BrdU-labeling experiments revealed that IR-induced damaged cells are preferentially eliminated, at least partially, in a tissue-dependent manner. Unexpectedly, the accumulation of damaged cells was found to occur independent from the DNA damage response modulator p53, and from an intact immune system, as their levels were similar in wild-type and Rag2(-/-) gammaC(-/-) mice, the latter being deficient in T, B, and NK cells. Together, our results provide compelling evidence that exposure to IR induces long-term expression of senescence markers in vivo, an effect that may contribute to the reduced tissue functionality observed in cancer survivors.

> **[43014661] Increased susceptibility to UV-induced skin carcinogenesis in polymerase eta-deficient mice.**
>
> Xeroderma pigmentosum variant (XPV) patients with mutations in the DNA polymerase eta (pol eta) gene are hypersensitive to sunlight and have greatly increased susceptibility to sunlight-induced skin cancer. Consistent with the ability of Pol eta to efficiently bypass UV light-induced cyclobutane pyrimidine dimers, XPV cells lacking Pol eta have diminished capacity to replicate UV-damaged DNA and are sensitive to UV light-induced killing and mutagenesis. To better understand these and other Pol eta functions, we generated Pol eta-deficient mice. Mice homozygous for a null mutation in pol eta are viable, fertile, and do not show any obvious spontaneous defects during the first year of life. However, fibroblasts derived from these mutant mice are sensitive to killing by exposure to UV light, and all Pol eta-deficient mice develop skin tumors after UV irradiation, in contrast to the wild-type littermate controls that did not develop such tumors. These results and biochemical studies of translesion synthesis by mouse Pol eta indicate that Pol eta-dependent bypass of cyclobutane pyrimidine dimers suppresses UV light-induced skin cancer in mice. Moreover, 37.5% of pol eta heterozygous mice also developed skin cancer during 5 months after a 5-month exposure to UV light, suggesting that humans who are heterozygous for mutations in pol eta may also have an increased risk of skin cancer.

> **[28441310] Mutation frequency and specificity with age in liver, bladder and brain of lacI transgenic mice.**
>
> Mutation frequency and specificity were determined as a function of age in nuclear DNA from liver, bladder, and brain of Big Blue lacI transgenic mice aged 1.5-25 months. Mutations accumulated with age in liver and accumulated more rapidly in bladder. In the brain a small initial increase in mutation frequency was observed in young animals; however, no further increase was observed in adult mice. To investigate the origin of mutations, the mutational spectra for each tissue and age were determined. DNA sequence analysis of mutant lacI transgenes revealed no significant changes in mutational specificity in any tissue at any age. The spectra of mutations found in aging animals were identical to those in younger animals, suggesting that they originated from a common set of DNA lesions manifested during DNA replication. The data also indicated that there were no significant age-related mutational changes due to oxidative damage, or errors resulting from either changes in the fidelity of DNA polymerase or the efficiency of DNA repair. Hence, no evidence was found to support hypotheses that predict that oxidative damage or accumulation of errors in nuclear DNA contributes significantly to the aging process, at least in these three somatic tissues.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-04 — faithfulness

**Claim:** Osteoparthritis (OA) is characterized by degeneration of articular cartilage, joint edge, and subchondral bone hyperplasia.

**Answer sentences:**

1. The provided abstracts do not mention subchondral bone hyperplasia as a characteristic of osteoarthritis (OA).
2. However, they do describe degenerative changes in articular cartilage, such as fibrillations, chondrocyte clusters, and degenerative matrix changes in OA [22505710].
3. The abstracts also mention changes in the infrapatellar fat pad and synovial fluid cytokine levels in OA, but they do not address subchondral bone hyperplasia [37562370, 45651303].

**Cited abstracts:**

> **[22505710] Matrix metalloproteinase and proinflammatory cytokine production by chondrocytes of human osteoarthritic cartilage: associations with degenerative changes.**
>
> OBJECTIVE To examine by immunohistochemistry the relative distributions of 6 matrix metalloproteinases (MMPs 1, 2, 3, 8, 9, and 13) and the 2 proinflammatory cytokines interleukin-1beta (IL-1beta) and tumor necrosis factor alpha (TNFalpha) in osteoarthritic (OA) cartilage compared with normal, age-matched articular cartilage. METHODS Articular cartilage samples were obtained from the tibial plateau of OA knees removed at arthroplasty and from normal, nonarthritic, knees obtained at autopsy. Specimens were promptly fixed in Carnoy's fixative, processed, embedded in paraffin, sectioned, and examined by immunohistochemistry for MMP and cytokine production. In addition, human articular chondrocytes (HAC) were treated in vitro with either IL-1beta, TNFalpha, or phorbol myristate acetate (PMA) to assess their potential to produce each of the MMPs, as determined by Western blotting and gelatin zymography. RESULTS Immunodetection of the collagenases (MMPs 1, 8, and 13) and stromelysin 1 (MMP-3) was demonstrated in a proportion of chondrocytes in the superficial zone of almost all of the OA specimens that had degenerative matrix changes. The gelatinases (MMPs 2 and 9) were also demonstrated by immunohistochemistry but were not so prominent. IL-1beta- and TNFalpha-positive chondrocytes were also observed in a proportion of cells in the superficial zones of OA specimens. Much less immunostaining for MMPs and cytokines was observed in the deep zone of all OA specimens, where the cartilage matrix and chondrocyte morphology appeared normal. In contrast, full-thickness normal cartilage specimens showed virtually no immunostaining for these MMPs or cytokines. Confirmation that chondrocytes can produce these 6 MMPs was obtained from HAC cultures treated with either IL-1beta, TNFalpha, or PMA; conditioned medium from activated HAC contained all the MMPs demonstrated by immunohistochemistry. Dual immunolocalization studies of OA cartilage specimens demonstrated the coexpression of IL-1 with MMP-8 by individual chondrocytes in situ. CONCLUSION These results indicate that the superficial zone of OA cartilage specimens, which is characterized by fibrillations, chondrocyte clusters, and degenerative matrix changes, contains a variable proportion of cells that immunostain for IL-1beta, TNFalpha, and 6 different MMPs. These observations support the concept that cytokine-MMP associations reflect a modified chondrocyte phenotype and an intrinsic process of cartilage degradation in OA.

> **[37562370] Cellular and histopathological changes in the infrapatellar fat pad in the monoiodoacetate model of osteoarthritis pain.**
>
> OBJECTIVE The infrapatellar fat pad (IPFP) has been identified as a source of anterior knee pain. Fibrosis and marked inflammatory infiltrate in the IPFP of patients with arthritis of the knee and reduction in pain post knee replacement in patients following resection of the IPFP have been observed. We have investigated changes in the IPFP of rats undergoing the monoiodoacetate (MIA) model of degenerative joint disease, a model that exhibits some histopathological similarities to osteoarthritis (OA). METHODS Rats were injected intra-articularly with MIA and the development of weight bearing asymmetry was followed for 21 days as compared to vehicle-injected animals. In addition, IPFPs were removed from both ipsilateral and contralateral joints. Both inflammatory infiltrate and histopathological changes were analysed. RESULTS MIA injection caused marked weight bearing asymmetry. Ipsilateral IPFP wet weights were significantly increased on days 1 and 3 in MIA-treated animals. MIA treatment also resulted in significant increases in IPFP total white blood cells and monocytes on days 1, 3, and 7 and neutrophils on days 1 and 3. This was supported by histopathological findings at early time points which progressed to adipocyte necrosis, IPFP fibrosis, patellar cartilage and subchondral bone necrosis with synovial hyperplasia at later timepoints. CONCLUSIONS The current study clearly demonstrated that marked inflammatory changes in the IPFP occur during the early stage of the MIA model of OA which may contribute to the pain observed at this early stage. The role of the IPFP in later stages of the model needs to be further explored.

> **[45651303] Interleukin-6 and interleukin-8 levels in serum and synovial fluid of patients with osteoarthritis.**
>
> Concentrations of interleukin (IL)-6 and IL-8 in serum and synovial fluid obtained from patients with osteoarthritis (OA) of the knee were determined by the chemiluminescence-ELISA (CL-ELISA) method, the sensitivity of which is 100-1,000 times greater than that of the conventional ELISA method. The results were compared with those obtained from patients with rheumatoid arthritis (RA) and from healthy subjects. The mean IL-6 and IL-8 levels in synovial fluid indicated higher concentrations in RA than in OA. The IL-6 and IL-8 levels in serum were significantly higher in RA and OA relative to controls. Among OA patients in whom remarkable improvement was noted in hydrarthrosis, the synovial fluid IL-6 and IL-8 levels at the initial examination were relatively higher, and were markedly decreased after treatment with sodium hyaluronate (NaHA). Among those in whom no improvement was noted in hydrarthrosis, the synovial fluid IL-6 and IL-8 levels at the time of initial examination were relatively lower, and hydrarthrosis was not significantly improved even after treatment with NaHA. In addition, there was a tendency for the synovial fluid IL-6 and IL-8 levels to decrease as HA levels increased. Evaluation of X-ray findings revealed that the IL-6 levels in synovial fluid at the initial examination in low-grade cases tended to be significantly higher than in high-grade cases. In low-grade cases, as determined by X-ray findings, there was a significant decrease in IL-6 levels in synovial fluid after treatment with NaHA.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-05 — abstention

**Claim:** IFIT1 speeds viral replication by allowing for the proliferation of mis-capped viral RNAs.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[10559501] Beta interferon controls West Nile virus infection and pathogenesis in mice.**
>
> Studies with mice lacking the common plasma membrane receptor for type I interferon (IFN-αβR(-)(/)(-)) have revealed that IFN signaling restricts tropism, dissemination, and lethality after infection with West Nile virus (WNV) or several other pathogenic viruses. However, the specific functions of individual IFN subtypes remain uncertain. Here, using IFN-β(-)(/)(-) mice, we defined the antiviral and immunomodulatory function of this IFN subtype in restricting viral infection. IFN-β(-)(/)(-) mice were more vulnerable to WNV infection than wild-type mice, succumbing more quickly and with greater overall mortality, although the phenotype was less severe than that of IFN-αβR(-)(/)(-) mice. The increased susceptibility of IFN-β(-)(/)(-) mice was accompanied by enhanced viral replication in different tissues. Consistent with a direct role for IFN-β in control of WNV replication, viral titers in ex vivo cultures of macrophages, dendritic cells, fibroblasts, and cerebellar granule cell neurons, but not cortical neurons, from IFN-β(-)(/)(-) mice were greater than in wild-type cells. Although detailed immunological analysis revealed no major deficits in the quality or quantity of WNV-specific antibodies or CD8(+) T cells, we observed an altered CD4(+) CD25(+) FoxP3(+) regulatory T cell response, with greater numbers after infection. Collectively, these results suggest that IFN-β controls WNV pathogenesis by restricting infection in key cell types and by modulating T cell regulatory networks.

> **[3308636] Interferons: Success in anti-viral immunotherapy.**
>
> The interferons (IFNs) are glycoproteins with strong antiviral activities that represent one of the first lines of host defense against invading pathogens. These proteins are classified into three groups, Type I, II and III IFNs, based on the structure of their receptors on the cell surface. Due to their ability to modulate immune responses, they have become attractive therapeutic options to control chronic virus infections. In combination with other drugs, Type I IFNs are considered as "standard of care" in suppressing Hepatitis C (HCV) and Hepatitis B (HBV) infections, while Type III IFN has generated encouraging results as a treatment for HCV infection in phase III clinical trials. However, though effective, using IFNs as a treatment is not without the need for caution. IFNs are such powerful cytokines that affect a wide array of cell types; as a result, patients usually experience unpleasant symptoms, with a percentage of patients suffering system wide effects. Thus, constant monitoring is required for patients treated with IFN in order to reach the treatment goals of suppressing virus infection and maintaining quality of life.

> **[5137019] Suppressor of cytokine signaling 3 inhibits antiviral IFN-beta signaling to enhance HIV-1 replication in macrophages.**
>
> HIV-1 replication within macrophages of the CNS often results in cognitive and motor impairment, which is known as HIV-associated dementia (HAD) in its most severe form. IFN-beta suppresses viral replication within these cells during early CNS infection, but the effect is transient. HIV-1 eventually overcomes this protective innate immune response to resume replication through an unknown mechanism, initiating the progression toward HAD. In this article, we show that Suppressor of Cytokine Signaling (SOCS)3, a molecular inhibitor of IFN signaling, may allow HIV-1 to evade innate immunity within the CNS. We found that SOCS3 is elevated in an in vivo SIV/macaque model of HAD and that the pattern of expression correlates with recurrence of viral replication and onset of CNS disease. In vitro, the HIV-1 regulatory protein transactivator of transcription induces SOCS3 in human and murine macrophages in a NF-kappaB-dependent manner. SOCS3 expression attenuates the response of macrophages to IFN-beta at proximal levels of pathway activation and downstream antiviral gene expression and consequently overcomes the inhibitory effect of IFN-beta on HIV-1 replication. These studies indicate that SOCS3 expression, induced by stimuli present in the HIV-1-infected brain, such as transactivator of transcription, inhibits antiviral IFN-beta signaling to enhance HIV-1 replication in macrophages. This consequence of SOCS3 expression in vitro, supported by a correlation with increased viral load and onset of CNS disease in vivo, suggests that SOCS3 may allow HIV-1 to evade the protective innate immune response within the CNS, allowing the recurrence of viral replication and, ultimately, promoting progression toward HAD.

> **[26731863] Distinct and essential roles of transcription factors IRF-3 and IRF-7 in response to viruses for IFN-alpha/beta gene induction.**
>
> Induction of the interferon (IFN)-alpha/beta gene transcription in virus-infected cells is an event central to innate immunity. Mice lacking the transcription factor IRF-3 are more vulnerable to virus infection. In embryonic fibroblasts, virus-induced IFN-alpha/beta gene expression levels are reduced and the spectrum of the IFN-alpha mRNA subspecies altered. Furthermore, cells additionally defective in IRF-7 expression totally fail to induce these genes in response to infections by any of the virus types tested. In these cells, a normal profile of IFN-alpha/beta mRNA induction can be achieved by coexpressing both IRF-3 and IRF-7. These results demonstrate the essential and distinct roles of thetwo factors, which together ensure the transcriptional efficiency and diversity of IFN-alpha/beta genes for the antiviral response.

> **[3493623] Suppression of interferon-mediated anti-HBV response by single CpG methylation in the 5′-UTR of TRIM22**
>
> Objective Interferons (IFNs) mediate direct antiviral activity. They play a crucial role in the early host immune response against viral infections. However, IFN therapy for HBV infection is less effective than for other viral infections. Design We explored the cellular targets of HBV in response to IFNs using proteome-wide screening. Results Using LC-MS/MS, we identified proteins downregulated and upregulated by IFN treatment in HBV X protein (HBx)-stable and control cells. We found several IFN-stimulated genes downregulated by HBx, including TRIM22, which is known as an antiretroviral protein. We demonstrated that HBx suppresses the transcription of TRIM22 through a single CpG methylation in its 5′-UTR, which further reduces the IFN regulatory factor-1 binding affinity, thereby suppressing the IFN-stimulated induction of TRIM22. Conclusions We verified our findings using a mouse model, primary human hepatocytes and human liver tissues. Our data elucidate a mechanism by which HBV evades the host innate immune system.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-06 — faithfulness

**Claim:** Integrated care is successful at tackling multiple comorbidities.

**Answer sentences:**

1. Integrated care is successful at tackling multiple comorbidities, as shown by a randomized trial where integrated care for chronic physical diseases and depression significantly reduced disability and improved quality of life [15041758].
2. The study demonstrated that integrated care can lead to better outcomes for patients with multiple conditions.

**Cited abstracts:**

> **[15041758] Functional outcomes of multi-condition collaborative care and successful ageing: results of randomised trial**
>
> OBJECTIVE To evaluate the effectiveness of integrated care for chronic physical diseases and depression in reducing disability and improving quality of life. DESIGN A randomised controlled trial of multi-condition collaborative care for depression and poorly controlled diabetes and/or risk factors for coronary heart disease compared with usual care among middle aged and elderly people   SETTING Fourteen primary care clinics in Seattle, Washington.   PARTICIPANTS Patients with diabetes or coronary heart disease, or both, and blood pressure above 140/90 mm Hg, low density lipoprotein concentration >3.37 mmol/L, or glycated haemoglobin 8.5% or higher, and PHQ-9 depression scores of ≥ 10. INTERVENTION A 12 month intervention to improve depression, glycaemic control, blood pressure, and lipid control by integrating a "treat to target" programme for diabetes and risk factors for coronary heart disease with collaborative care for depression. The intervention combined self management support, monitoring of disease control, and pharmacotherapy to control depression, hyperglycaemia, hypertension, and hyperlipidaemia. MAIN OUTCOME MEASURES Social role disability (Sheehan disability scale), global quality of life rating, and World Health Organization disability assessment schedule (WHODAS-2) scales to measure disabilities in activities of daily living (mobility, self care, household maintenance). RESULTS Of 214 patients enrolled (106 intervention and 108 usual care), disability and quality of life measures were obtained for 97 intervention patients at six months (92%) and 92 at 12 months (87%), and for 96 usual care patients at six months (89%) and 92 at 12 months (85%). Improvements from baseline on the Sheehan disability scale (-0.9, 95% confidence interval -1.5 to -0.2; P = 0.006) and global quality of life rating (0.7, 0.2 to 1.2; P = 0.005) were significantly greater at six and 12 months in patients in the intervention group. There was a trend toward greater improvement in disabilities in activities of daily living (-1.5, -3.3 to 0.4; P = 0.10). CONCLUSIONS Integrated care that covers chronic physical disease and comorbid depression can reduce social role disability and enhance global quality of life. Trial registration Clinical Trials NCT00468676.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-07 — abstention

**Claim:** Transcription rates in S. cerevisiae range between 7 and 12 kb/min.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[365896] RiboSys, a high-resolution, quantitative approach to measure the in vivo kinetics of pre-mRNA splicing and 3'-end processing in Saccharomyces cerevisiae.**
>
> We describe methods for obtaining a quantitative description of RNA processing at high resolution in budding yeast. As a model gene expression system, we constructed tetON (for induction studies) and tetOFF (for repression, derepression, and RNA degradation studies) yeast strains with a series of reporter genes integrated in the genome under the control of a tetO7 promoter. Reverse transcription and quantitative real-time-PCR (RT-qPCR) methods were adapted to allow the determination of mRNA abundance as the average number of copies per cell in a population. Fluorescence in situ hybridization (FISH) measurements of transcript numbers in individual cells validated the RT-qPCR approach for the average copy-number determination despite the broad distribution of transcript levels within a population of cells. In addition, RT-qPCR was used to distinguish the products of the different steps in splicing of the reporter transcripts, and methods were developed to map and quantify 3'-end cleavage and polyadenylation. This system permits pre-mRNA production, splicing, 3'-end maturation and degradation to be quantitatively monitored with unprecedented kinetic detail, suitable for mathematical modeling. Using this approach, we demonstrate that reporter transcripts are spliced prior to their 3'-end cleavage and polyadenylation, that is, cotranscriptionally.

> **[16237005] Single-RNA counting reveals alternative modes of gene expression in yeast**
>
> Proper execution of transcriptional programs is a key requirement of gene expression regulation, demanding accurate control of timing and amplitude. How precisely the transcription machinery fulfills this task is not known. Using an in situ hybridization approach that detects single mRNA molecules, we measured mRNA abundance and transcriptional activity within single Saccharomyces cerevisiae cells. We found that expression levels for particular genes are higher than initially reported and can vary substantially among cells. However, variability for most constitutively expressed genes is unexpectedly small. Combining single-transcript measurements with computational modeling indicates that low expression variation is achieved by transcribing genes using single transcription-initiation events that are clearly separated in time, rather than by transcriptional bursts. In contrast, PDR5, a gene regulated by the transcription coactivator complex SAGA, is expressed using transcription bursts, resulting in larger variation. These data directly demonstrate the existence of multiple expression modes used to modulate the transcriptome.

> **[2817000] Histone Variant H2A.Z Marks the 5′ Ends of Both Active and Inactive Genes in Euchromatin**
>
> In S. cerevisiae, histone variant H2A.Z is deposited in euchromatin at the flanks of silent heterochromatin to prevent its ectopic spread. We show that H2A.Z nucleosomes are found at promoter regions of nearly all genes in euchromatin. They generally occur as two positioned nucleosomes that flank a nucleosome-free region (NFR) that contains the transcription start site. Astonishingly, enrichment at 5' ends is observed not only at actively transcribed genes but also at inactive loci. Mutagenesis of a typical promoter revealed a 22 bp segment of DNA sufficient to program formation of a NFR flanked by two H2A.Z nucleosomes. This segment contains a binding site of the Myb-related protein Reb1 and an adjacent dT:dA tract. Efficient deposition of H2A.Z is further promoted by a specific pattern of histone H3 and H4 tail acetylation and the bromodomain protein Bdf1, a component of the Swr1 remodeling complex that deposits H2A.Z.

> **[36606083] Quantitative, genome-wide analysis of eukaryotic replication initiation and termination.**
>
> Many fundamental aspects of DNA replication, such as the exact locations where DNA synthesis is initiated and terminated, how frequently origins are used, and how fork progression is influenced by transcription, are poorly understood. Via the deep sequencing of Okazaki fragments, we comprehensively document replication fork directionality throughout the S. cerevisiae genome, which permits the systematic analysis of initiation, origin efficiency, fork progression, and termination. We show that leading-strand initiation preferentially occurs within a nucleosome-free region at replication origins. Using a strain in which late origins can be induced to fire early, we show that replication termination is a largely passive phenomenon that does not rely on cis-acting sequences or replication fork pausing. The replication profile is predominantly determined by the kinetics of origin firing, allowing us to reconstruct chromosome-wide timing profiles from an asynchronous culture.

> **[41811327] At least 1400 base pairs of 5'-flanking DNA is required for the correct expression of the HO gene in yeast.**
>
> Homothallic yeast cells undergo a specific pattern of mating-type switching initiated by an endonuclease encoded by the HO gene. HO transcription is affected by cell type (a, alpha, and a/alpha), by cell age (mother or daughter), and by the cell cycle. This paper investigates the sequences involved in HO transcription by replacing genomic DNA with copies mutated in vitro. A region between -1000 and 1400 (called URS1) is necessary for transcription in addition to a "TATA"-like region at -90. The 900 bp of DNA separating URS1 from the "TATA" box is not necessary for transcription nor for a/alpha repression and some measure of mother/daughter control, but it is necessary for correct cell cycle control.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-08 — faithfulness

**Claim:** Clathrin stabilizes the spindle fiber apparatus during mitosis.

**Answer sentences:**

1. Clathrin stabilizes fibres of the mitotic spindle to aid congression of chromosomes, as shown by the depletion of clathrin heavy chain leading to destabilized kinetochore fibres and defective congression [2033917].

**Cited abstracts:**

> **[2033917] Clathrin is required for the function of the mitotic spindle**
>
> Clathrin has an established function in the generation of vesicles that transfer membrane and proteins around the cell. The formation of clathrin-coated vesicles occurs continuously in non-dividing cells, but is shut down during mitosis, when clathrin concentrates at the spindle apparatus. Here, we show that clathrin stabilizes fibres of the mitotic spindle to aid congression of chromosomes. Clathrin bound to the spindle directly by the amino-terminal domain of clathrin heavy chain. Depletion of clathrin heavy chain using RNA interference prolonged mitosis; kinetochore fibres were destabilized, leading to defective congression of chromosomes to the metaphase plate and persistent activation of the spindle checkpoint. Normal mitosis was rescued by clathrin triskelia but not the N-terminal domain of clathrin heavy chain, indicating that stabilization of kinetochore fibres was dependent on the unique structure of clathrin. The importance of clathrin for normal mitosis may be relevant to understanding human cancers that involve gene fusions of clathrin heavy chain.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-09 — faithfulness

**Claim:** Lamins are associated with nuclear membrane structure maintenance.

**Answer sentences:**

1. Lamins are associated with nuclear membrane structure maintenance, as evidenced by the role of lamin A in the nuclear structural defects observed in Hutchinson-Gilford progeria syndrome [34747208].
2. Additionally, lamin B1 interacts with the autophagy protein LC3/Atg8, which is involved in maintaining nuclear lamina components [4452659].
3. The loss of lamin B1 leads to changes in nuclear structure, including decondensation of chromosome territories and increased nuclear blebs [25036988].
4. These findings support the involvement of lamins in the maintenance of nuclear membrane structure.

**Cited abstracts:**

> **[34747208] Lamin A-dependent nuclear defects in human aging.**
>
> Mutations in the nuclear structural protein lamin A cause the premature aging syndrome Hutchinson-Gilford progeria (HGPS). Whether lamin A plays any role in normal aging is unknown. We show that the same molecular mechanism responsible for HGPS is active in healthy cells. Cell nuclei from old individuals acquire defects similar to those of HGPS patient cells, including changes in histone modifications and increased DNA damage. Age-related nuclear defects are caused by sporadic use, in healthy individuals, of the same cryptic splice site in lamin A whose constitutive activation causes HGPS. Inhibition of this splice site reverses the nuclear defects associated with aging. These observations implicate lamin A in physiological aging.

> **[4452659] Autophagy mediates degradation of nuclear lamina**
>
> Macroautophagy (hereafter referred to as autophagy) is a catabolic membrane trafficking process that degrades a variety of cellular constituents and is associated with human diseases. Although extensive studies have focused on autophagic turnover of cytoplasmic materials, little is known about the role of autophagy in degrading nuclear components. Here we report that the autophagy machinery mediates degradation of nuclear lamina components in mammals. The autophagy protein LC3/Atg8, which is involved in autophagy membrane trafficking and substrate delivery, is present in the nucleus and directly interacts with the nuclear lamina protein lamin B1, and binds to lamin-associated domains on chromatin. This LC3-lamin B1 interaction does not downregulate lamin B1 during starvation, but mediates its degradation upon oncogenic insults, such as by activated RAS. Lamin B1 degradation is achieved by nucleus-to-cytoplasm transport that delivers lamin B1 to the lysosome. Inhibiting autophagy or the LC3-lamin B1 interaction prevents activated RAS-induced lamin B1 loss and attenuates oncogene-induced senescence in primary human cells. Our study suggests that this new function of autophagy acts as a guarding mechanism protecting cells from tumorigenesis.

> **[25036988] Loss of lamin B1 results in prolongation of S phase and decondensation of chromosome territories.**
>
> Nuclear lamin B1 (LMNB1) constitutes one of the major structural proteins in the lamina mesh. We silenced the expression of LMNB1 by RNA interference in the colon cancer cell line DLD-1 and showed a dramatic redistribution of H3K27me3 from the periphery to a more homogeneous nuclear dispersion. In addition, we observed telomere attrition and an increased frequency of micronuclei and nuclear blebs. By 3D-FISH analyses, we demonstrated that the volume and surface of chromosome territories were significantly larger in LMNB1-depleted cells, suggesting that LMNB1 is required to maintain chromatin condensation in interphase nuclei. These changes led to a prolonged S phase due to activation of Chk1. Finally, silencing of LMNB1 resulted in extensive changes in alternative splicing of multiple genes and in a higher number of enlarged nuclear speckles. Taken together, our results suggest a mechanistic role of the nuclear lamina in the organization of chromosome territories, maintenance of genome integrity and proper gene splicing.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-10 — abstention

**Claim:** Mice defective for deoxyribonucleic acid (DNA) polymerase I (polI) fail to reveal increased sensitivity to ionizing radiation (IR).

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[11569583] Deregulated DNA polymerase β strengthens ionizing radiation-induced nucleotidic and chromosomal instabilities**
>
> DNA polymerase β (Pol β) is an error-prone enzyme which has been found to be overexpressed in several human tumors. By using a couple of recombinant CHO cells differing only from the exogenous expression of Pol β, we showed here that cells overexpressing Pol β are much more sensitive to IR treatments by increasing apoptosis. We also found that the surviving cells displayed an hypermutator phenotype which could be explained by different pathways involving Pol β, such as (i) an increased capacity to incorporate into DNA the mutagenic dGTP analog, 8-oxo-dGTP, one of the most abundant purine-derived nucleotides exposed to γ-irradiation, (ii) the induction of IR-induced DNA breaks and (iii) accumulation of chromosome aberrations induced by radiation. Alteration of Pol β expression in irradiated cells thus appears to strengthen both cell death and genetic changes associated with a malignant phenotype. These data provide new insights into the cellular response to radiations and the associated carcinogenic consequences.

> **[27635177] Association of DNA polymerase mu (pol mu) with Ku and ligase IV: role for pol mu in end-joining double-strand break repair.**
>
> Mammalian DNA polymerase mu (pol mu) is related to terminal deoxynucleotidyl transferase, but its biological role is not yet clear. We show here that after exposure of cells to ionizing radiation (IR), levels of pol mu protein increase. pol mu also forms discrete nuclear foci after IR, and these foci are largely coincident with IR-induced foci of gammaH2AX, a previously characterized marker of sites of DNA double-strand breaks. pol mu is thus part of the cellular response to DNA double-strand breaks. pol mu also associates in cell extracts with the nonhomologous end-joining repair factor Ku and requires both Ku and another end-joining factor, XRCC4-ligase IV, to form a stable complex on DNA in vitro. pol mu in turn facilitates both stable recruitment of XRCC4-ligase IV to Ku-bound DNA and ligase IV-dependent end joining. In contrast, the related mammalian DNA polymerase beta does not form a complex with Ku and XRCC4-ligase IV and is less effective than pol mu in facilitating joining mediated by these factors. Our data thus support an important role for pol mu in the end-joining pathway for repair of double-strand breaks.

> **[31293581] Ionizing radiation-induced long-term expression of senescence markers in mice is independent of p53 and immune status.**
>
> Exposure to IR has been shown to induce the formation of senescence markers, a phenotype that coincides with lifelong delayed repair and regeneration of irradiated tissues. We hypothesized that IR-induced senescence markers could persist long-term in vivo, possibly contributing to the permanent reduction in tissue functionality. Here, we show that mouse tissues exposed to a sublethal dose of IR display persistent (up to 45 weeks, the maximum time analyzed) DNA damage foci and increased p16(INK4a) expression, two hallmarks of cellular senescence and aging. BrdU-labeling experiments revealed that IR-induced damaged cells are preferentially eliminated, at least partially, in a tissue-dependent manner. Unexpectedly, the accumulation of damaged cells was found to occur independent from the DNA damage response modulator p53, and from an intact immune system, as their levels were similar in wild-type and Rag2(-/-) gammaC(-/-) mice, the latter being deficient in T, B, and NK cells. Together, our results provide compelling evidence that exposure to IR induces long-term expression of senescence markers in vivo, an effect that may contribute to the reduced tissue functionality observed in cancer survivors.

> **[43014661] Increased susceptibility to UV-induced skin carcinogenesis in polymerase eta-deficient mice.**
>
> Xeroderma pigmentosum variant (XPV) patients with mutations in the DNA polymerase eta (pol eta) gene are hypersensitive to sunlight and have greatly increased susceptibility to sunlight-induced skin cancer. Consistent with the ability of Pol eta to efficiently bypass UV light-induced cyclobutane pyrimidine dimers, XPV cells lacking Pol eta have diminished capacity to replicate UV-damaged DNA and are sensitive to UV light-induced killing and mutagenesis. To better understand these and other Pol eta functions, we generated Pol eta-deficient mice. Mice homozygous for a null mutation in pol eta are viable, fertile, and do not show any obvious spontaneous defects during the first year of life. However, fibroblasts derived from these mutant mice are sensitive to killing by exposure to UV light, and all Pol eta-deficient mice develop skin tumors after UV irradiation, in contrast to the wild-type littermate controls that did not develop such tumors. These results and biochemical studies of translesion synthesis by mouse Pol eta indicate that Pol eta-dependent bypass of cyclobutane pyrimidine dimers suppresses UV light-induced skin cancer in mice. Moreover, 37.5% of pol eta heterozygous mice also developed skin cancer during 5 months after a 5-month exposure to UV light, suggesting that humans who are heterozygous for mutations in pol eta may also have an increased risk of skin cancer.

> **[12552297] The DNA polymerase λ is required for the repair of non-compatible DNA double strand breaks by NHEJ in mammalian cells**
>
> DNA polymerase lambda (polλ) is a recently identified DNA polymerase whose cellular function remains elusive. Here we show, that polλ participates at the molecular level in a chromosomal context, in the repair of DNA double strand breaks (DSB) via non-homologous end joining (NHEJ) in mammalian cells. The expression of a catalytically inactive form of polλ (polλDN) decreases the frequency of NHEJ events in response to I-Sce-I-induced DSB whereas inactivated forms of its homologues polβ and polμ do not. Only events requiring DNA end processing before ligation are affected; this defect is associated with large deletions arising in the vicinity of the induced DSB. Furthermore, polλDN-expressing cells exhibit increased sensitization and genomic instability in response to ionizing radiation similar to that of NHEJ-defective cells. Our data support a requirement for polλ in repairing a subset of DSB in genomic DNA, thereby contributing to the maintenance of genetic stability mediated by the NHEJ pathway.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-11 — abstention

**Claim:** The DESMOND program demonstrates no significant impact on weight loss.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[7552215] Long term pharmacotherapy for obesity and overweight: updated meta-analysis.**
>
> OBJECTIVE To summarise the long term efficacy of anti-obesity drugs in reducing weight and improving health status. DESIGN Updated meta-analysis of randomised trials. DATA SOURCES Medline, Embase, the Cochrane controlled trials register, the Current Science meta-register of controlled trials, and reference lists of identified articles. All data sources were searched from December 2002 (end date of last search) to December 2006. STUDIES REVIEWED Double blind randomised placebo controlled trials of approved anti-obesity drugs used in adults (age over 18) for one year or longer. RESULTS 30 trials of one to four years' duration met the inclusion criteria: 16 orlistat (n=10 631 participants), 10 sibutramine (n=2623), and four rimonabant (n=6365). Of these, 14 trials were new and 16 had previously been identified. Attrition rates averaged 30-40%. Compared with placebo, orlistat reduced weight by 2.9 kg (95% confidence interval 2.5 kg to 3.2 kg), sibutramine by 4.2 kg (3.6 kg to 4.7 kg), and rimonabant by 4.7 kg (4.1 kg to 5.3 kg). Patients receiving active drug treatment were significantly more likely to achieve 5% and 10% weight loss thresholds. Orlistat reduced the incidence of diabetes and improved concentrations of total cholesterol and low density lipoprotein cholesterol, blood pressure, and glycaemic control in patients with diabetes but increased rates of gastrointestinal side effects and slightly lowered concentrations of high density lipoprotein. Sibutramine improved [corrected] concentrations of high density lipoprotein cholesterol and triglycerides [corrected] Rimonabant improved concentrations of high density lipoprotein cholesterol and triglycerides, blood pressure, and glycaemic control in patients with diabetes but increased the risk of mood disorders. CONCLUSIONS Orlistat, sibutramine, and rimonabant modestly reduce weight, have differing effects on cardiovascular risk profiles, and have specific adverse effects.

> **[32322418] Moderate regular exercise increases basal production of nitric oxide in elderly women.**
>
> Vascular endothelial cells produce nitric oxide (NO), which is a potent vasodilator substance and is thought to have antiatherosclerotic properties. Therefore, it has also been proposed that NO may be useful to regulate vascular tonus and prevent progression of atherosclerosis. On the other hand, NO activity reduces with aging. We previously reported that the plasma nitrite/nitrate (NOx: the stable end product of NO) concentration was significantly increased by intense aerobic exercise training in healthy young humans. We hypothesized that lifestyle modification (e.g., even mild regular exercise training) can increase NO production in previously sedentary older humans. We measured the plasma NOx concentration before and after a mild aerobic exercise training regimen (cycling on a leg ergometer at 80% ventilatory threshold for 30 min, 5 days/week) for 3 months in elderly women. In addition, we assessed the plasma concentration of cyclic guanosine monophosphate (cGMP), a second messenger of NO, in the same samples. The individual ventilatory threshold increased significantly after the 3-month exercise training. The blood pressure at rest significantly decreased after exercise training. These results suggest that the 3-month exercise training in the older women produced favorable physiological effects. The plasma concentration of NOx significantly increased by the exercise training, and the plasma concentration of cGMP also increased by the exercise training. The present study suggests that even a mild regular aerobic-endurance exercise increases NO production in previously sedentary older humans, which may have beneficial effects (i.e., antihypertensive and antiatherosclerotic effects by endogenous NO) on the cardiovascular system.

> **[6841927] Transtheoretical model-based multiple behavior intervention for weight management: effectiveness on a population basis.**
>
> BACKGROUND The increasing prevalence of overweight and obesity underscores the need for evidence-based, easily disseminable interventions for weight management that can be delivered on a population basis. The Transtheoretical Model (TTM) offers a promising theoretical framework for multiple behavior weight management interventions. METHODS Overweight or obese adults (BMI 25-39.9; n=1277) were randomized to no-treatment control or home-based, stage-matched multiple behavior interventions for up to three behaviors related to weight management at 0, 3, 6, and 9 months. All participants were re-assessed at 6, 12, and 24 months. RESULTS Significant treatment effects were found for healthy eating (47.5% versus 34.3%), exercise (44.90% versus 38.10%), managing emotional distress (49.7% versus 30.30%), and untreated fruit and vegetable intake (48.5% versus 39.0%) progressing to Action/Maintenance at 24 months. The groups differed on weight lost at 24 months. Co-variation of behavior change occurred and was much more pronounced in the treatment group, where individuals progressing to Action/Maintenance for a single behavior were 2.5-5 times more likely to make progress on another behavior. The impact of the multiple behavior intervention was more than three times that of single behavior interventions. CONCLUSIONS This study demonstrates the ability of TTM-based tailored feedback to improve healthy eating, exercise, managing emotional distress, and weight on a population basis. The treatment produced a high level of population impact that future multiple behavior interventions can seek to surpass.

> **[11360768] Effects of interventions in pregnancy on maternal weight and obstetric outcomes: meta-analysis of randomised evidence**
>
> OBJECTIVE To evaluate the effects of dietary and lifestyle interventions in pregnancy on maternal and fetal weight and to quantify the effects of these interventions on obstetric outcomes. DESIGN Systematic review and meta-analysis. DATA SOURCES Major databases from inception to January 2012 without language restrictions. STUDY SELECTION Randomised controlled trials that evaluated any dietary or lifestyle interventions with potential to influence maternal weight during pregnancy and outcomes of pregnancy. DATA SYNTHESIS Results summarised as relative risks for dichotomous data and mean differences for continuous data. RESULTS We identified 44 relevant randomised controlled trials (7278 women) evaluating three categories of interventions: diet, physical activity, and a mixed approach. Overall, there was 1.42 kg reduction (95% confidence interval 0.95 to 1.89 kg) in gestational weight gain with any intervention compared with control. With all interventions combined, there were no significant differences in birth weight (mean difference -50 g, -100 to 0 g) and the incidence of large for gestational age (relative risk 0.85, 0.66 to 1.09) or small for gestational age (1.00, 0.78 to 1.28) babies between the groups, though by itself physical activity was associated with reduced birth weight (mean difference -60 g, -120 to -10 g). Interventions were associated with a reduced the risk of pre-eclampsia (0.74, 0.60 to 0.92) and shoulder dystocia (0.39, 0.22 to 0.70), with no significant effect on other critically important outcomes. Dietary intervention resulted in the largest reduction in maternal gestational weight gain (3.84 kg, 2.45 to 5.22 kg), with improved pregnancy outcomes compared with other interventions. The overall evidence rating was low to very low for important outcomes such as pre-eclampsia, gestational diabetes, gestational hypertension, and preterm delivery. CONCLUSIONS Dietary and lifestyle interventions in pregnancy can reduce maternal gestational weight gain and improve outcomes for both mother and baby. Among the interventions, those based on diet are the most effective and are associated with reductions in maternal gestational weight gain and improved obstetric outcomes.

> **[41310252] Dietary fat and obesity: evidence from epidemiology.**
>
> The epidemiological evidence that a high-fat diet promotes the development of obesity is considered suggestive but not definitive. The purpose of this paper is to provide a review of various epidemiological methods that have been used to address this issue as well as an updated summary of the existing evidence. Ecological studies describing dietary fat intake and obesity at the population level provide mixed results and are likely to be biased by both confounding and unknown data quality factors that differ systematically across the populations studied. Cross-sectional studies are generally in agreement that the concentration of fat in the diet is positively associated with relative weight. Prospective studies of diet in relation to subsequent weight change give inconsistent results. This may be due to behavioural factors such as dieting in response to weight gain; in addition, this type of study rarely takes into account the possible interaction between genetic predisposition and dietary fat in promoting weight gain. Finally, intervention studies in free-living subjects are considered, providing evidence of a consistent but short-lived period of active weight loss on low-fat diets. The experimental evidence on this relationship is more conclusive than the epidemiological evidence, although biological mechanisms remain controversial. Some areas for future epidemiological research involve: longitudinal studies of dietary fat intake as a predictor of growth in children; observational studies relating total dietary fat and specific types of fat to overall as well as regional adiposity; and randomized intervention studies of the effect of low-fat diets with particular emphasis on and familial predisposition to obesity and other possible modifying factors.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-12 — abstention

**Claim:** The one-child policy has created a hospitable environment for female infants.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[108886332] Training toddlers seated on mobile robots to drive indoors amidst obstacles**
>
> The goal of this research is to train children seated on mobile robots to purposefully and safely drive indoors. Our previous studies show that in about six weeks of training, infants can learn to drive directly to a goal using conventional joysticks. However, they are unable to acquire the advanced skill to avoid obstacles while driving. This limits mobility impaired children from exploring their home environment safely, which in turn impacts their cognitive and social developments in the important early years. In this paper, we describe results where toddlers are trained to drive a robot within an obstacle course. Using algorithms based on artificial potential fields to avoid obstacles, we create force field on the joystick that trains them to navigate while avoiding obstacles. In this ‘assist-as-needed’ approach, if the child steers the mobile robot outside a force tunnel centered around the desired direction, the driver experiences a bias force on the hand. The results suggest that force-feedback joystick results in faster learning than with a conventional joystick.

> **[42291761] Preventing deaths by drowning in children in the United Kingdom: have we made progress in 10 years? Population based incidence study.**
>
> Detailed information on drowning in children is not routinely collected by offices of national statistics. Few studies have been carried out in the United Kingdom, and none has been done on British children abroad. In 1988-9, two of the authors (AMK and JRS) combined information from national statistical offices, police forces (Royal Life Saving Society), and from a press cutting service (Royal Society for Prevention of Accidents) for a detailed analysis of deaths by drowning in children.1, 2, 3 This analysis found that 149 children had drowned in the United Kingdom during 1998-9. It also identified a safety agenda, which focused on young children in garden ponds and pools and on older children swimming without supervision. Over the past 10 years there have been initiatives on children's safety in water, particularly swimming. We obtained similar information for 1998-9 to identify changes that have …

> **[23531592] Paediatric HIV infection.**
>
> By the year 2000 there will be six million pregnant women and five to ten million children infected with HIV-1. Intervention strategies have been planned and in some instances already started. A timely and cost-effective strategy needs to take into account that most HIV-1 infected individuals reside in developing countries. Further studies are needed on immunological and virological factors affecting HIV-1 transmission from mother to child, on differential disease progression in affected children, and on transient infection.

> **[17877537] Babies driving robots: self-generated mobility in very young infants**
>
> Self-generated mobility via locomotion is a key for the cognitive, social and motor development of young infants. For certain children with special needs, self-generated mobility is only attained via assistive technology such as a power wheelchair. Up until recently, infants under 24 months of age were not considered candidates for training in power mobility. Recent work in our labs and others suggest that younger infants can utilize their reaching and grasping ability to learn power mobility. This interdisciplinary study combines our previous work in motor development and learning in infants with special needs, and the application of robot technology for rehabilitation to determine whether young infants without structured training, would drive a mobile robot, and if so, to determine how their driving would change over multiple sessions. The two infants that were seen for the most sessions were the focus of this pilot study. Both infants increased their total session time, percentage of session time spent driving, and total path length. These results suggest that, without training, young infants will independently move themselves using a mobile robot. These results provide the foundation for training studies to advance the self-generated mobility in young infants with special needs. Our future studies will explore the multiple training and technology combinations to reduce the barriers to exploration via self-generated mobility, and advance the general development of infants with special needs.

> **[16204011] Care Seeking for Neonatal Illness in Low- and Middle-Income Countries: A Systematic Review**
>
> BACKGROUND Despite recent achievements to reduce child mortality, neonatal deaths continue to remain high, accounting for 41% of all deaths in children under five years of age worldwide, of which over 90% occur in low- and middle-income countries (LMICs). Infections are a leading cause of death and limitations in care seeking for ill neonates contribute to high mortality rates. As estimates for care-seeking behaviors in LMICs have not been studied, this review describes care seeking for neonatal illnesses in LMICs, with particular attention to type of care sought. METHODS AND FINDINGS We conducted a systematic literature review of studies that reported the proportion of caregivers that sought care for ill or suspected ill neonates in LMICs. The initial search yielded 784 studies, of which 22 studies described relevant data from community household surveys, facility-based surveys, and intervention trials. The majority of studies were from South Asia (n = 17/22), set in rural areas (n = 17/22), and published within the last 4 years (n = 18/22). Of the 9,098 neonates who were ill or suspected to be ill, 4,320 caregivers sought some type of care, including care from a health facility (n = 370) or provider (n = 1,813). Care seeking ranged between 10% and 100% among caregivers with a median of 59%. Care seeking from a health care provider yielded a similar range and median, while care seeking at a health care facility ranged between 1% and 100%, with a median of 20%. Care-seeking estimates were limited by the few studies conducted in urban settings and regions other than South Asia. There was a lack of consistency regarding illness, care-seeking, and care provider definitions. CONCLUSIONS There is a paucity of data regarding newborn care-seeking behaviors; in South Asia, care seeking is low for newborn illness, especially in terms of care sought from health care facilities and medically trained providers. There is a need for representative data to describe care-seeking patterns in different geographic regions and better understand mechanisms to enhance care seeking during this vulnerable time period.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-13 — abstention

**Claim:** Activator-inhibitor pairs are provided ventrally by Xrl-sizzled.

**Answer:** The provided abstracts do not mention Xrl-sizzled or its role as an activator-inhibitor pair ventrally. [NOT_FOUND]

**All retrieved abstracts:**

> **[6076903] Regulation of ADMP and BMP2/4/7 at Opposite Embryonic Poles Generates a Self-Regulating Morphogenetic Field**
>
> Embryos have the ability to self-regulate and regenerate normal structures after being sectioned in half. How is such a morphogenetic field established? We discovered that quadruple knockdown of ADMP and BMP2/4/7 in Xenopus embryos eliminates self-regulation, causing ubiquitous neural induction throughout the ectoderm. ADMP transcription in the Spemann organizer is activated at low BMP levels. When ventral BMP2/4/7 signals are depleted, Admp expression increases, allowing for self-regulation. ADMP has BMP-like activity and signals via the ALK-2 receptor. It is unable to signal dorsally because of inhibition by Chordin. The ventral BMP antagonists Sizzled and Bambi further refine the pattern. By transplanting dorsal or ventral wild-type grafts into ADMP/BMP2/4/7-depleted hosts, we demonstrate that both poles serve as signaling centers that can induce histotypic differentiation over considerable distances. We conclude that dorsal and ventral BMP signals and their extracellular antagonists expressed under opposing transcriptional regulation provide a molecular mechanism for embryonic self-regulation.

> **[19485649] N- and E-cadherins in Xenopus are specifically required in the neural and non-neural ectoderm, respectively, for F-actin assembly and morphogenetic movements.**
>
> Transmembrane cadherins are calcium-dependent intercellular adhesion molecules. Recently, they have also been shown to be sites of actin assembly during adhesive contact formation. However, the roles of actin assembly on transmembrane cadherins during development are not fully understood. We show here, using the developing ectoderm of the Xenopus embryo as a model, that F-actin assembly is a primary function of both N-cadherin in the neural ectoderm and E-cadherin in the non-neural (epidermal) ectoderm, and that each cadherin is essential for the characteristic morphogenetic movements of these two tissues. However, depletion of N-cadherin and E-cadherin did not cause dissociation in these tissues at the neurula stage, probably owing to the expression of C-cadherin in each tissue. Depletion of each of these cadherins is not rescued by the other, nor by the expression of C-cadherin, which is expressed in both tissues. One possible reason for this is that each cadherin is expressed in a different domain of the cell membrane. These data indicate the combinatorial nature of cadherin function, the fact that N- and E-cadherin play primary roles in F-actin assembly in addition to roles in cell adhesion, and that this function is specific to individual cadherins. They also show how cell adhesion and motility can be combined in morphogenetic tissue movements that generate the form and shape of the embryonic organs.

> **[14492964] The Spemann Organizer Signal noggin Binds and Inactivates Bone Morphogenetic Protein 4**
>
> Signals released by the Spemann organizer of the amphibian gastrula can directly induce neural tissue from ectoderm and can dorsalize ventral mesoderm to form muscle. The secreted polypeptide noggin mimics these activities and is expressed at the appropriate time and place to participate in the organizer signal. Neural induction and mesoderm dorsalization are antagonized by bone morphogenetic proteins (BMPs), which induce epidermis and ventral mesoderm instead. Here we report that noggin protein binds BMP4 with high affinity and can abolish BMP4 activity by blocking binding to cognate cell-surface receptors. These data suggest that noggin secreted by the organizer patterns the embryo by interrupting BMP signaling.

> **[40383969] The structure of the follistatin:activin complex reveals antagonism of both type I and type II receptor binding.**
>
> TGF-beta ligands stimulate diverse cellular differentiation and growth responses by signaling through type I and II receptors. Ligand antagonists, such as follistatin, block signaling and are essential regulators of physiological responses. Here we report the structure of activin A, a TGF-beta ligand, bound to the high-affinity antagonist follistatin. Two follistatin molecules encircle activin, neutralizing the ligand by burying one-third of its residues and its receptor binding sites. Previous studies have suggested that type I receptor binding would not be blocked by follistatin, but the crystal structure reveals that the follistatin N-terminal domain has an unexpected fold that mimics a universal type I receptor motif and occupies this receptor binding site. The formation of follistatin:BMP:type I receptor complexes can be explained by the stoichiometric and geometric arrangement of the activin:follistatin complex. The mode of ligand binding by follistatin has important implications for its ability to neutralize homo- and heterodimeric ligands of this growth factor family.

> **[8997410] Arp2/3 complex inhibition radically alters lamellipodial actin architecture, suspended cell shape, and the cell spreading process**
>
> Recent studies have investigated the dendritic actin cytoskeleton of the cell edge's lamellipodial (LP) region by experimentally decreasing the activity of the actin filament nucleator and branch former, the Arp2/3 complex. Here we extend these studies via pharmacological inhibition of the Arp2/3 complex in sea urchin coelomocytes, cells that possess an unusually broad LP region and display correspondingly exaggerated centripetal flow. Using light and electron microscopy, we demonstrate that Arp2/3 complex inhibition via the drug CK666 dramatically altered LP actin architecture, slowed centripetal flow, drove a lamellipodial-to-filopodial shape change in suspended cells, and induced a novel actin structural organization during cell spreading. A general feature of the CK666 phenotype in coelomocytes was transverse actin arcs, and arc generation was arrested by a formin inhibitor. We also demonstrate that CK666 treatment produces actin arcs in other cells with broad LP regions, namely fish keratocytes and Drosophila S2 cells. We hypothesize that the actin arcs made visible by Arp2/3 complex inhibition in coelomocytes may represent an exaggerated manifestation of the elongate mother filaments that could possibly serve as the scaffold for the production of the dendritic actin network.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-14 — abstention

**Claim:** Activator-inhibitor pairs are provided ventrally by Xrl-sizzled.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[36921186] Derivation conditions impact X-inactivation status in female human induced pluripotent stem cells.**
>
> Female human induced pluripotent stem cell (hiPSC) lines exhibit variability in X-inactivation status. The majority of hiPSC lines maintain one transcriptionally active X (Xa) and one inactive X (Xi) chromosome from donor cells. However, at low frequency, hiPSC lines with two Xas are produced, suggesting that epigenetic alterations of the Xi occur sporadically during reprogramming. We show here that X-inactivation status in female hiPSC lines depends on derivation conditions. hiPSC lines generated by the Kyoto method (retroviral or episomal reprogramming), which uses leukemia inhibitory factor (LIF)-expressing SNL feeders, frequently had two Xas. Early passage Xa/Xi hiPSC lines generated on non-SNL feeders were converted into Xa/Xa hiPSC lines after several passages on SNL feeders, and supplementation with recombinant LIF caused reactivation of some of X-linked genes. Thus, feeders are a significant factor affecting X-inactivation status. The efficient production of Xa/Xa hiPSC lines provides unprecedented opportunities to understand human X-reactivation and -inactivation.

> **[19485649] N- and E-cadherins in Xenopus are specifically required in the neural and non-neural ectoderm, respectively, for F-actin assembly and morphogenetic movements.**
>
> Transmembrane cadherins are calcium-dependent intercellular adhesion molecules. Recently, they have also been shown to be sites of actin assembly during adhesive contact formation. However, the roles of actin assembly on transmembrane cadherins during development are not fully understood. We show here, using the developing ectoderm of the Xenopus embryo as a model, that F-actin assembly is a primary function of both N-cadherin in the neural ectoderm and E-cadherin in the non-neural (epidermal) ectoderm, and that each cadherin is essential for the characteristic morphogenetic movements of these two tissues. However, depletion of N-cadherin and E-cadherin did not cause dissociation in these tissues at the neurula stage, probably owing to the expression of C-cadherin in each tissue. Depletion of each of these cadherins is not rescued by the other, nor by the expression of C-cadherin, which is expressed in both tissues. One possible reason for this is that each cadherin is expressed in a different domain of the cell membrane. These data indicate the combinatorial nature of cadherin function, the fact that N- and E-cadherin play primary roles in F-actin assembly in addition to roles in cell adhesion, and that this function is specific to individual cadherins. They also show how cell adhesion and motility can be combined in morphogenetic tissue movements that generate the form and shape of the embryonic organs.

> **[40383969] The structure of the follistatin:activin complex reveals antagonism of both type I and type II receptor binding.**
>
> TGF-beta ligands stimulate diverse cellular differentiation and growth responses by signaling through type I and II receptors. Ligand antagonists, such as follistatin, block signaling and are essential regulators of physiological responses. Here we report the structure of activin A, a TGF-beta ligand, bound to the high-affinity antagonist follistatin. Two follistatin molecules encircle activin, neutralizing the ligand by burying one-third of its residues and its receptor binding sites. Previous studies have suggested that type I receptor binding would not be blocked by follistatin, but the crystal structure reveals that the follistatin N-terminal domain has an unexpected fold that mimics a universal type I receptor motif and occupies this receptor binding site. The formation of follistatin:BMP:type I receptor complexes can be explained by the stoichiometric and geometric arrangement of the activin:follistatin complex. The mode of ligand binding by follistatin has important implications for its ability to neutralize homo- and heterodimeric ligands of this growth factor family.

> **[14492964] The Spemann Organizer Signal noggin Binds and Inactivates Bone Morphogenetic Protein 4**
>
> Signals released by the Spemann organizer of the amphibian gastrula can directly induce neural tissue from ectoderm and can dorsalize ventral mesoderm to form muscle. The secreted polypeptide noggin mimics these activities and is expressed at the appropriate time and place to participate in the organizer signal. Neural induction and mesoderm dorsalization are antagonized by bone morphogenetic proteins (BMPs), which induce epidermis and ventral mesoderm instead. Here we report that noggin protein binds BMP4 with high affinity and can abolish BMP4 activity by blocking binding to cognate cell-surface receptors. These data suggest that noggin secreted by the organizer patterns the embryo by interrupting BMP signaling.

> **[18855191] Exploitative and Hierarchical Antagonism in a Cooperative Bacterium**
>
> Social organisms that cooperate with some members of their own species, such as close relatives, may fail to cooperate with other genotypes of the same species. Such noncooperation may take the form of outright antagonism or social exploitation. Myxococcus xanthus is a highly social prokaryote that cooperatively develops into spore-bearing, multicellular fruiting bodies in response to starvation. Here we have characterized the nature of social interactions among nine developmentally proficient strains of M. xanthus isolated from spatially distant locations. Strains were competed against one another in all possible pairwise combinations during starvation-induced development. In most pairings, at least one competitor exhibited strong antagonism toward its partner and a majority of mixes showed bidirectional antagonism that decreased total spore production, even to the point of driving whole populations to extinction. Differential response to mixing was the primary determinant of competitive superiority rather than the sporulation efficiencies of unmixed populations. In some competitive pairings, the dominant partner sporulated more efficiently in mixed populations than in clonal isolation. This finding represents a novel form of exploitation in bacteria carried out by socially competent genotypes and is the first documentation of social exploitation among natural bacterial isolates. Patterns of antagonistic superiority among these strains form a highly linear dominance hierarchy. At least some competition pairs construct chimeric, rather than segregated, fruiting bodies. The cooperative prokaryote M. xanthus has diverged into a large number of distinct social types that cooperate with clone-mates but exhibit intense antagonism toward distinct social types of the same species. Most lengthy migration events in nature may thus result in strong antagonism between migratory and resident populations, and this antagonism may have large effects on local population sizes and dynamics. Intense mutual antagonism appears to be more prevalent in this prokaryotic social species than has been observed in the eukaryotic social slime mold Dictyostelium discoideum, which also exhibits multicellular development. The finding of several cases of facultative social exploitation among these natural isolates suggests that such exploitation may occur frequently in nature in many prokaryotes with cooperative traits.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-15 — abstention

**Claim:** Deleting Raptor increases G-CSF levels.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[22174015] PI3K-Akt-mTORC1-S6K1/2 axis controls Th17 differentiation by regulating Gfi1 expression and nuclear translocation of RORγ.**
>
> The PI3K-Akt-mTORC1 axis contributes to the activation, survival, and proliferation of CD4(+) T cells upon stimulation through TCR and CD28. Here, we demonstrate that the suppression of this axis by deletion of p85α or PI3K/mTORC1 inhibitors as well as T cell-specific deletion of raptor, an essential component of mTORC1, impairs Th17 differentiation in vitro and in vivo in a S6K1/2-dependent fashion. Inhibition of PI3K-Akt-mTORC1-S6K1 axis impairs the downregulation of Gfi1, a negative regulator of Th17 differentiation. Furthermore, we demonstrate that S6K2, a nuclear counterpart of S6K1, is induced by the PI3K-Akt-mTORC1 axis, binds RORγ, and carries RORγ to the nucleus. These results point toward a pivotal role of PI3K-Akt-mTORC1-S6K1/2 axis in Th17 differentiation.

> **[6962472] G*Power 3: a flexible statistical power analysis program for the social, behavioral, and biomedical sciences.**
>
> G*Power (Erdfelder, Faul, & Buchner, 1996) was designed as a general stand-alone power analysis program for statistical tests commonly used in social and behavioral research. G*Power 3 is a major extension of, and improvement over, the previous versions. It runs on widely used computer platforms (i.e., Windows XP, Windows Vista, and Mac OS X 10.4) and covers many different statistical tests of the t, F, and chi2 test families. In addition, it includes power analyses for z tests and some exact tests. G*Power 3 provides improved effect size calculators and graphic options, supports both distribution-based and design-based input modes, and offers all types of power analyses in which users might be interested. Like its predecessors, G*Power 3 is free.

> **[10790846] A rapamycin-sensitive signaling pathway contributes to long-term synaptic plasticity in the hippocampus.**
>
> Many forms of long-lasting behavioral and synaptic plasticity require the synthesis of new proteins. For example, long-term potentiation (LTP) that endures for more than an hour requires both transcription and translation. The signal-transduction mechanisms that couple synaptic events to protein translational machinery during long-lasting synaptic plasticity, however, are not well understood. One signaling pathway that is stimulated by growth factors and results in the translation of specific mRNAs includes the rapamycin-sensitive kinase mammalian target of rapamycin (mTOR, also known as FRAP and RAFT-1). Several components of this translational signaling pathway, including mTOR, eukaryotic initiation factor-4E-binding proteins 1 and 2, and eukaryotic initiation factor-4E, are present in the rat hippocampus as shown by Western blot analysis, and these proteins are detected in the cell bodies and dendrites in the hippocampal slices by immunostaining studies. In cultured hippocampal neurons, these proteins are present in dendrites and are often found near the presynaptic protein, synapsin I. At synaptic sites, their distribution completely overlaps with a postsynaptic protein, PSD-95. These observations suggest the postsynaptic localization of these proteins. Disruption of mTOR signaling by rapamycin results in a reduction of late-phase LTP expression induced by high-frequency stimulation; the early phase of LTP is unaffected. Rapamycin also blocks the synaptic potentiation induced by brain-derived neurotrophic factor in hippocampal slices. These results demonstrate an essential role for rapamycin-sensitive signaling in the expression of two forms of synaptic plasticity that require new protein synthesis. The localization of this translational signaling pathway at postsynaptic sites may provide a mechanism that controls local protein synthesis at potentiated synapses.

> **[2014909] Oncogenic mTOR signaling recruits myeloid-derived suppressor cells to promote tumor initiation**
>
> Myeloid-derived suppressor cells (MDSCs) play critical roles in primary and metastatic cancer progression. MDSC regulation is widely variable even among patients harbouring the same type of malignancy, and the mechanisms governing such heterogeneity are largely unknown. Here, integrating human tumour genomics and syngeneic mammary tumour models, we demonstrate that mTOR signalling in cancer cells dictates a mammary tumour's ability to stimulate MDSC accumulation through regulating G-CSF. Inhibiting this pathway or its activators (for example, FGFR) impairs tumour progression, which is partially rescued by restoring MDSCs or G-CSF. Tumour-initiating cells (TICs) exhibit elevated G-CSF. MDSCs reciprocally increase TIC frequency through activating Notch in tumour cells, forming a feedforward loop. Analyses of primary breast cancers and patient-derived xenografts corroborate these mechanisms in patients. These findings establish a non-canonical oncogenic role of mTOR signalling in recruiting pro-tumorigenic MDSCs and show how defined cancer subsets may evolve to promote and depend on a distinct immune microenvironment.

> **[4658268] Rictor, a Novel Binding Partner of mTOR, Defines a Rapamycin-Insensitive and Raptor-Independent Pathway that Regulates the Cytoskeleton**
>
> The mammalian TOR (mTOR) pathway integrates nutrient- and growth factor-derived signals to regulate growth, the process whereby cells accumulate mass and increase in size. mTOR is a large protein kinase and the target of rapamycin, an immunosuppressant that also blocks vessel restenosis and has potential anticancer applications. mTOR interacts with the raptor and GbetaL proteins to form a complex that is the target of rapamycin. Here, we demonstrate that mTOR is also part of a distinct complex defined by the novel protein rictor (rapamycin-insensitive companion of mTOR). Rictor shares homology with the previously described pianissimo from D. discoidieum, STE20p from S. pombe, and AVO3p from S. cerevisiae. Interestingly, AVO3p is part of a rapamycin-insensitive TOR complex that does not contain the yeast homolog of raptor and signals to the actin cytoskeleton through PKC1. Consistent with this finding, the rictor-containing mTOR complex contains GbetaL but not raptor and it neither regulates the mTOR effector S6K1 nor is it bound by FKBP12-rapamycin. We find that the rictor-mTOR complex modulates the phosphorylation of Protein Kinase C alpha (PKCalpha) and the actin cytoskeleton, suggesting that this aspect of TOR signaling is conserved between yeast and mammals.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-16 — faithfulness

**Claim:** Tumor development occurs in conjunction with suppression of pro-inflammatory cytokines.

**Answer sentences:**

1. The provided abstracts do not directly address the suppression of pro-inflammatory cytokines in conjunction with tumor development.
2. Instead, they describe the promotion of tumor development by pro-inflammatory cytokines such as IL-17 and the role of inflammatory environments in tumor progression [25726838, 4429118].
3. The abstracts do not mention suppression of pro-inflammatory cytokines in the context of tumor development.
4. Therefore, the claim is not supported by the given abstracts.

**Cited abstracts:**

> **[25726838] IL-17 promotes tumor development through the induction of tumor promoting microenvironments at tumor sites and myeloid-derived suppressor cells.**
>
> The role of immune responses in tumor development is a central issue for tumor biology and immunology. IL-17 is an important cytokine for inflammatory and autoimmune diseases. Although IL-17-producing cells are detected in cancer patients and tumor-bearing mice, the role of IL-17 in tumor development is controversial, and mechanisms remain to be fully elucidated. In the current study, we found that the development of tumors was inhibited in IL-17R-deficient mice. A defect in IFN-gammaR increased tumor growth, whereas tumor growth was inhibited in mice that were deficient in both IL-17R and IFN-gammaR compared with wild-type animals. Further experiments showed that neutralization of IL-17 by Abs inhibited tumor growth in wild-type mice, whereas systemic administration of IL-17 promoted tumor growth. The IL-17R deficiency increased CD8 T cell infiltration, whereas it reduced the infiltration of myeloid-derived suppressor cells (MDSCs) in tumors. In contrast, administration of IL-17 inhibited CD8 T cell infiltration and increased MDSCs in tumors. Further analysis indicated that IL-17 was required for the development and tumor-promoting activity of MDSCs in tumor-bearing mice. These data demonstrate that IL-17-mediated responses promote tumor development through the induction of tumor-promoting microenvironments at tumor sites. IL-17-mediated regulation of MDSCs is a primary mechanism for its tumor-promoting effects. The study provides novel insights into the role of IL-17 in tumor development and has major implications for targeting IL-17 in treatment of tumors.

> **[4429118] Cancer-related inflammation**
>
> The mediators and cellular effectors of inflammation are important constituents of the local environment of tumours. In some types of cancer, inflammatory conditions are present before a malignant change occurs. Conversely, in other types of cancer, an oncogenic change induces an inflammatory microenvironment that promotes the development of tumours. Regardless of its origin, 'smouldering' inflammation in the tumour microenvironment has many tumour-promoting effects. It aids in the proliferation and survival of malignant cells, promotes angiogenesis and metastasis, subverts adaptive immune responses, and alters responses to hormones and chemotherapeutic agents. The molecular pathways of this cancer-related inflammation are now being unravelled, resulting in the identification of new target molecules that could lead to improved diagnosis and treatment.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-17 — faithfulness

**Claim:** Sympathetic nerve activity is reduced throughout normal pregnancy.

**Answer sentences:**

1. The evidence contradicts the claim.
2. Sympathetic nerve activity is increased during normal pregnancy, as shown by higher muscle sympathetic nerve activity (MSNA) in pregnant women compared to nonpregnant controls [5323845].
3. Additionally, studies have found increased sympathetic activation during early pregnancy and in the third trimester of normotensive pregnancy [26710772, 13907928].
4. These findings indicate that sympathetic nerve activity is not reduced but rather elevated throughout normal pregnancy.

**Cited abstracts:**

> **[5323845] Sympathetic neural mechanisms in normal and hypertensive pregnancy in humans.**
>
> BACKGROUND Direct recordings from peripheral sympathetic nerves have shown an increased sympathetic drive in pregnancy-induced hypertension (PIH) and preeclampsia (PE). It is unknown whether sympathetic drive is altered in normal pregnancy, when arterial blood pressure can be normal or relatively low. The aim of this study was to measure and compare peripheral sympathetic discharge, its vasoconstrictor effect and its baroreceptor control, during pregnancy and postpartum in women with normal pregnancy (NP) and PIH and in normotensive nonpregnant (NN) women. METHODS AND RESULTS Twenty-one women with NP, 18 women with PIH, and 21 NN women had muscle sympathetic nerve activity assessed from multiunit discharges (MSNA) and from single units with defined vasoconstrictor properties (s-MSNA). The s-MSNA in NP (38+/-6.6 impulses/100 beats) was greater (P<0.05) than in NN women (19+/-1.8 impulses/100 beats) despite similar age and body weight but less than in PIH women (P<0.001) (146+/-23.5 impulses/100 beats). MSNA followed a similar trend. Cardiac baroreceptor reflex sensitivity (BRS) was impaired in NP and PIH women relative to NN. After delivery, sympathetic activity decreased to values similar to those obtained in NN, and there was an increase in BRS. In women with NP, the decrease in sympathetic output occurred despite an insignificant change in blood pressure. CONCLUSIONS Central sympathetic output was increased in women with normal pregnancy and was even greater in the hypertensive pregnant group. The findings suggest that the moderate sympathetic hyperactivity during the latter months of normal pregnancy may help to return the arterial pressure to nonpregnant levels, although when the increase in activity is excessive, hypertension may ensue.

> **[26710772] Sympathetic activation during early pregnancy in humans.**
>
> Sympathetic activity has been reported to increase in normotensive pregnant women, and to be even greater in women with gestational hypertension and preeclampsia at term. Whether sympathetic overactivity develops early during pregnancy, remaining high throughout gestation, or whether it only occurs at term providing the substrate for hypertensive disorders is unknown. We tested the hypothesis that sympathetic activation occurs early during pregnancy in humans. Eleven healthy women (29 ± 3 (SD) years) without prior hypertensive pregnancies were tested during the mid-luteal phase (PRE) and early pregnancy (EARLY; 6.2 ± 1.2 weeks of gestation). Muscle sympathetic nerve activity (MSNA) and haemodynamics were measured supine, at 30 deg and 60 deg upright tilt for 5 min each. Blood samples were drawn for catecholamines, direct renin, and aldosterone. MSNA was significantly greater during EARLY than PRE (supine: 25 ± 8 vs. 14 ± 8 bursts min(-1), 60 deg tilt: 49 ± 14 vs. 40 ± 10 bursts min(-1); main effect, P < 0.05). Resting diastolic pressure trended lower (P = 0.09), heart rate was similar, total peripheral resistance decreased (2172 ± 364 vs. 2543 ± 352 dyne s cm(-5); P < 0.05), sympathetic vascular transduction was blunted (0.10 ± 0.05 vs. 0.36 ± 0.47 units a.u.(-1) min(-1); P < 0.01), and both renin (supine: 27.9 ± 6.2 vs. 14.2 ± 8.7 pg ml(-1), P < 0.01) and aldosterone (supine: 16.7 ± 14.1 vs. 7.7 ± 6.8 ng ml(-1), P = 0.05) were higher during EARLY than PRE. These results suggest that sympathetic activation is a common characteristic of early pregnancy in humans despite reduced diastolic pressure and total peripheral resistance. These observations challenge conventional thinking about blood pressure regulation during pregnancy, showing marked sympathetic activation occurring within the first few weeks of conception, and may provide the substrate for pregnancy induced cardiovascular complications.

> **[13907928] Regulation of sympathetic nerve activity during the cold pressor test in normotensive pregnant and nonpregnant women.**
>
> Baseline neurovascular transduction is reduced in normotensive pregnancy; however, little is known about changes to neurovascular transduction during periods of heightened sympathetic activation. We tested the hypothesis that, despite an exacerbated muscle sympathetic nerve activity (microneurography) response to cold pressor stimulation, the blunting of neurovascular transduction in normotensive pregnant women would result in similar changes in vascular resistance and mean arterial pressure (Finometer) relative to nonpregnant controls. Baseline neurovascular transduction was reduced in pregnant women relative to controls when expressed as the quotient of both total resistance and mean arterial pressure and sympathetic burst frequency (0.32±0.07 versus 0.58±0.16 mm Hg/L/min/bursts/min, P<0.001 and 2.4±0.7 versus 3.6±0.8 mm Hg/bursts/min, P=0.001). Sympathetic activation was greater across all 3 minutes of cold pressor stimulation in the pregnant women relative to the nonpregnant controls. Peak sympathoexcitation was also greater in pregnant than in nonpregnant women, whether expressed as sympathetic burst frequency (+17±13 versus +7±8 bursts/min, P=0.049), burst incidence (+17±9 versus +6±11 bursts/100 hb, P=0.03), or total activity (+950±660 versus +363±414 arbitrary units, P=0.04). However, neurovascular transduction during peak cold pressor-induced sympathoexcitation remained blunted in pregnant women (0.25±0.11 versus 0.45±0.08 mm Hg/L/min/bursts/min, P<0.001 and 1.9±1.0 versus 3.2±0.9 mm Hg/bursts/min, P=0.006). Therefore, mean arterial pressure (93±21 versus 99±6 mm Hg, P=0.4) and total peripheral resistance (12±3 versus 14±3 mm Hg/L/min) were not different between pregnant and nonpregnant women during peak sympathoexcitation. These data indicate that the third trimester of normotensive pregnancy is associated with reductions in neurovascular transduction, which result in the dissociation of sympathetic outflow from hemodynamic outcomes, even during cold pressor-induced sympathoexcitation.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-18 — faithfulness

**Claim:** Tumor development occurs in conjunction with suppression of pro-inflammatory cytokines.

**Answer sentences:**

1. The provided abstracts do not directly address the suppression of pro-inflammatory cytokines in conjunction with tumor development.
2. However, they do discuss the role of specific cytokines, such as IL-17, in promoting tumor development through the induction of tumor-promoting microenvironments and the regulation of myeloid-derived suppressor cells [25726838].
3. Abstracts also highlight the role of inflammation in tumor development, indicating that inflammation can be a tumorigenic factor [4429118].
4. There is no evidence provided that supports the claim that tumor development occurs in conjunction with the suppression of pro-inflammatory cytokines.

**Cited abstracts:**

> **[25726838] IL-17 promotes tumor development through the induction of tumor promoting microenvironments at tumor sites and myeloid-derived suppressor cells.**
>
> The role of immune responses in tumor development is a central issue for tumor biology and immunology. IL-17 is an important cytokine for inflammatory and autoimmune diseases. Although IL-17-producing cells are detected in cancer patients and tumor-bearing mice, the role of IL-17 in tumor development is controversial, and mechanisms remain to be fully elucidated. In the current study, we found that the development of tumors was inhibited in IL-17R-deficient mice. A defect in IFN-gammaR increased tumor growth, whereas tumor growth was inhibited in mice that were deficient in both IL-17R and IFN-gammaR compared with wild-type animals. Further experiments showed that neutralization of IL-17 by Abs inhibited tumor growth in wild-type mice, whereas systemic administration of IL-17 promoted tumor growth. The IL-17R deficiency increased CD8 T cell infiltration, whereas it reduced the infiltration of myeloid-derived suppressor cells (MDSCs) in tumors. In contrast, administration of IL-17 inhibited CD8 T cell infiltration and increased MDSCs in tumors. Further analysis indicated that IL-17 was required for the development and tumor-promoting activity of MDSCs in tumor-bearing mice. These data demonstrate that IL-17-mediated responses promote tumor development through the induction of tumor-promoting microenvironments at tumor sites. IL-17-mediated regulation of MDSCs is a primary mechanism for its tumor-promoting effects. The study provides novel insights into the role of IL-17 in tumor development and has major implications for targeting IL-17 in treatment of tumors.

> **[4429118] Cancer-related inflammation**
>
> The mediators and cellular effectors of inflammation are important constituents of the local environment of tumours. In some types of cancer, inflammatory conditions are present before a malignant change occurs. Conversely, in other types of cancer, an oncogenic change induces an inflammatory microenvironment that promotes the development of tumours. Regardless of its origin, 'smouldering' inflammation in the tumour microenvironment has many tumour-promoting effects. It aids in the proliferation and survival of malignant cells, promotes angiogenesis and metastasis, subverts adaptive immune responses, and alters responses to hormones and chemotherapeutic agents. The molecular pathways of this cancer-related inflammation are now being unravelled, resulting in the identification of new target molecules that could lead to improved diagnosis and treatment.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-19 — faithfulness

**Claim:** Cellular differentiation of embryonic stem cells is accompanied by changes in replication timing, transcription and nuclear localization.

**Answer sentences:**

1. Cellular differentiation of embryonic stem cells is accompanied by changes in replication timing, as shown by the consolidation of smaller replication domains into larger units during differentiation [8148122].
2. Changes in replication timing are also coordinated with transcription changes, particularly for weak promoters [8148122].
3. Additionally, replication-timing changes are accompanied by rearrangements in subnuclear position [8148122].
4. These findings support the claim that differentiation involves changes in replication timing, transcription, and nuclear localization.

**Cited abstracts:**

> **[8148122] Global Reorganization of Replication Domains During Embryonic Stem Cell Differentiation**
>
> DNA replication in mammals is regulated via the coordinate firing of clusters of replicons that duplicate megabase-sized chromosome segments at specific times during S-phase. Cytogenetic studies show that these "replicon clusters" coalesce as subchromosomal units that persist through multiple cell generations, but the molecular boundaries of such units have remained elusive. Moreover, the extent to which changes in replication timing occur during differentiation and their relationship to transcription changes has not been rigorously investigated. We have constructed high-resolution replication-timing profiles in mouse embryonic stem cells (mESCs) before and after differentiation to neural precursor cells. We demonstrate that chromosomes can be segmented into multimegabase domains of coordinate replication, which we call "replication domains," separated by transition regions whose replication kinetics are consistent with large originless segments. The molecular boundaries of replication domains are remarkably well conserved between distantly related ESC lines and induced pluripotent stem cells. Unexpectedly, ESC differentiation was accompanied by the consolidation of smaller differentially replicating domains into larger coordinately replicated units whose replication time was more aligned to isochore GC content and the density of LINE-1 transposable elements, but not gene density. Replication-timing changes were coordinated with transcription changes for weak promoters more than strong promoters, and were accompanied by rearrangements in subnuclear position. We conclude that replication profiles are cell-type specific, and changes in these profiles reveal chromosome segments that undergo large changes in organization during differentiation. Moreover, smaller replication domains and a higher density of timing transition regions that interrupt isochore replication timing define a novel characteristic of the pluripotent state.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-20 — faithfulness

**Claim:** Cellular differentiation of embryonic stem cells is accompanied by changes in replication timing, transcription and nuclear localization.

**Answer sentences:**

1. Cellular differentiation of embryonic stem cells is accompanied by changes in replication timing, as shown by the consolidation of smaller differentially replicating domains into larger coordinately replicated units [8148122].
2. Changes in replication timing are coordinated with transcription changes, particularly for weak promoters [8148122].
3. Additionally, these changes are accompanied by rearrangements in subnuclear position [8148122].
4. The study also highlights the relationship between replication timing and isochore GC content and LINE-1 transposable element density [8148122].

**Cited abstracts:**

> **[8148122] Global Reorganization of Replication Domains During Embryonic Stem Cell Differentiation**
>
> DNA replication in mammals is regulated via the coordinate firing of clusters of replicons that duplicate megabase-sized chromosome segments at specific times during S-phase. Cytogenetic studies show that these "replicon clusters" coalesce as subchromosomal units that persist through multiple cell generations, but the molecular boundaries of such units have remained elusive. Moreover, the extent to which changes in replication timing occur during differentiation and their relationship to transcription changes has not been rigorously investigated. We have constructed high-resolution replication-timing profiles in mouse embryonic stem cells (mESCs) before and after differentiation to neural precursor cells. We demonstrate that chromosomes can be segmented into multimegabase domains of coordinate replication, which we call "replication domains," separated by transition regions whose replication kinetics are consistent with large originless segments. The molecular boundaries of replication domains are remarkably well conserved between distantly related ESC lines and induced pluripotent stem cells. Unexpectedly, ESC differentiation was accompanied by the consolidation of smaller differentially replicating domains into larger coordinately replicated units whose replication time was more aligned to isochore GC content and the density of LINE-1 transposable elements, but not gene density. Replication-timing changes were coordinated with transcription changes for weak promoters more than strong promoters, and were accompanied by rearrangements in subnuclear position. We conclude that replication profiles are cell-type specific, and changes in these profiles reveal chromosome segments that undergo large changes in organization during differentiation. Moreover, smaller replication domains and a higher density of timing transition regions that interrupt isochore replication timing define a novel characteristic of the pluripotent state.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-21 — faithfulness

**Claim:** Interferon stimulated genes (ISGs) Irf1, Irg1, Ifi27, and Rsad2 inhibit West Nile virus replication in cortical neurons.

**Answer sentences:**

1. The abstracts do not directly state that ISGs Irf1, Irg1, Ifi27, and Rsad2 inhibit West Nile virus replication in cortical neurons.
2. However, they do mention that ISGs such as Ifi27, Irg1, and Rsad2 mediate antiviral effects against neurotropic viruses in granule cell neurons [9433958].
3. There is no specific information provided about the inhibition of West Nile virus replication in cortical neurons by these ISGs.

**Cited abstracts:**

> **[9433958] Differential innate immune response programs in neuronal subtypes determine susceptibility to infection in the brain by positive stranded RNA viruses**
>
> Although susceptibility of neurons in the brain to microbial infection is a major determinant of clinical outcome, little is known about the molecular factors governing this vulnerability. Here we show that two types of neurons from distinct brain regions showed differential permissivity to replication of several positive-stranded RNA viruses. Granule cell neurons of the cerebellum and cortical neurons from the cerebral cortex have unique innate immune programs that confer differential susceptibility to viral infection ex vivo and in vivo. By transducing cortical neurons with genes that were expressed more highly in granule cell neurons, we identified three interferon-stimulated genes (ISGs; Ifi27, Irg1 and Rsad2 (also known as Viperin)) that mediated the antiviral effects against different neurotropic viruses. Moreover, we found that the epigenetic state and microRNA (miRNA)-mediated regulation of ISGs correlates with enhanced antiviral response in granule cell neurons. Thus, neurons from evolutionarily distinct brain regions have unique innate immune signatures, which probably contribute to their relative permissiveness to infection.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-22 — faithfulness

**Claim:** Diminished ovarian reserve is a reliable indicator of infertility in a non-infertile population.

**Answer sentences:**

1. The claim that diminished ovarian reserve is a reliable indicator of infertility in a non-infertile population is not supported by the evidence presented in the abstracts.
2. The study [13497630] found that biomarkers indicating diminished ovarian reserve were not associated with reduced fertility among women aged 30 to 44 years without a history of infertility.
3. Therefore, the findings do not support the use of these biomarkers to assess natural fertility in this population.

**Cited abstracts:**

> **[13497630] Association Between Biomarkers of Ovarian Reserve and Infertility Among Older Women of Reproductive Age**
>
> Importance Despite lack of evidence of their utility, biomarkers of ovarian reserve are being promoted as potential markers of reproductive potential. Objective To determine the associations between biomarkers of ovarian reserve and reproductive potential among women of late reproductive age. Design, Setting, and Participants Prospective time-to-pregnancy cohort study (2008 to date of last follow-up in March 2016) of women (N = 981) aged 30 to 44 years without a history of infertility who had been trying to conceive for 3 months or less, recruited from the community in the Raleigh-Durham, North Carolina, area. Exposures Early-follicular-phase serum level of antimüllerian hormone (AMH), follicle-stimulating hormone (FSH), and inhibin B and urinary level of FSH. Main Outcomes and Measures The primary outcomes were the cumulative probability of conception by 6 and 12 cycles of attempt and relative fecundability (probability of conception in a given menstrual cycle). Conception was defined as a positive pregnancy test result. Results A total of 750 women (mean age, 33.3 [SD, 3.2] years; 77% white; 36% overweight or obese) provided a blood and urine sample and were included in the analysis. After adjusting for age, body mass index, race, current smoking status, and recent hormonal contraceptive use, women with low AMH values (<0.7 ng/mL [n = 84]) did not have a significantly different predicted probability of conceiving by 6 cycles of attempt (65%; 95% CI, 50%-75%) compared with women (n = 579) with normal values (62%; 95% CI, 57%-66%) or by 12 cycles of attempt (84% [95% CI, 70%-91%] vs 75% [95% CI, 70%-79%], respectively). Women with high serum FSH values (>10 mIU/mL [n = 83]) did not have a significantly different predicted probability of conceiving after 6 cycles of attempt (63%; 95% CI, 50%-73%) compared with women (n = 654) with normal values (62%; 95% CI, 57%-66%) or after 12 cycles of attempt (82% [95% CI, 70%-89%] vs 75% [95% CI, 70%-78%], respectively). Women with high urinary FSH values (>11.5 mIU/mg creatinine [n = 69]) did not have a significantly different predicted probability of conceiving after 6 cycles of attempt (61%; 95% CI, 46%-74%) compared with women (n = 660) with normal values (62%; 95% CI, 58%-66%) or after 12 cycles of attempt (70% [95% CI, 54%-80%] vs 76% [95% CI, 72%-80%], respectively). Inhibin B levels (n = 737) were not associated with the probability of conceiving in a given cycle (hazard ratio per 1-pg/mL increase, 0.999; 95% CI, 0.997-1.001). Conclusions and Relevance Among women aged 30 to 44 years without a history of infertility who had been trying to conceive for 3 months or less, biomarkers indicating diminished ovarian reserve compared with normal ovarian reserve were not associated with reduced fertility. These findings do not support the use of urinary or blood follicle-stimulating hormone tests or antimüllerian hormone levels to assess natural fertility for women with these characteristics.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-23 — faithfulness

**Claim:** Immune responses in immune cells are geographically segregated.

**Answer sentences:**

1. The concept of geographic segregation of immune responses is not directly addressed in the provided abstracts.
2. However, the abstracts do mention that immune cells communicate via cytokines, and the spatial extent of this communication is quantified in certain contexts [4928282].
3. Additionally, tissue-resident memory T cells are described as being specialized for local immunity, suggesting a degree of localization in immune responses [3155731].
4. These findings do not explicitly support or contradict the claim of geographic segregation.

**Cited abstracts:**

> **[4928282] A Tunable Diffusion‐Consumption Mechanism of Cytokine Propagation Enables Plasticity in Cell‐to‐Cell Communication in the Immune System**
>
> &NA; Immune cells communicate by exchanging cytokines to achieve a context‐appropriate response, but the distances over which such communication happens are not known. Here, we used theoretical considerations and experimental models of immune responses in vitro and in vivo to quantify the spatial extent of cytokine communications in dense tissues. We established that competition between cytokine diffusion and consumption generated spatial niches of high cytokine concentrations with sharp boundaries. The size of these self‐assembled niches scaled with the density of cytokine‐consuming cells, a parameter that gets tuned during immune responses. In vivo, we measured interactions on length scales of 80–120 &mgr;m, which resulted in a high degree of cell‐to‐cell variance in cytokine exposure. Such heterogeneous distributions of cytokines were a source of non‐genetic cell‐to‐cell variability that is often overlooked in single‐cell studies. Our findings thus provide a basis for understanding variability in the patterning of immune responses by diffusible factors. Graphical Abstract Figure. No caption available. HighlightsCytokine penetration in tissues is governed by a diffusion‐consumption mechanismSpherical cytokine niches are generated around cytokine‐producing cellsThe characteristic niche size depends on the density of cytokine consumersCytokine niches are a source of variability in otherwise identical cells &NA; Cytokine‐mediated communication allows immune cells to achieve a context‐appropriate response, but the distance over which this communication happens is unclear. Oyler‐Yaniv et al. (2017) show that a simple diffusion‐consumption mechanism quantitatively describes the spatial spread of cytokines in vivo and results in localized niches of high cytokine concentrations that contribute to cell‐to‐cell variability.

> **[3155731] Tissue-resident memory T cells: local specialists in immune defence**
>
> T cells have crucial roles in protection against infection and cancer. Although the trafficking of memory T cells around the body is integral to their capacity to provide immune protection, studies have shown that specialization of some memory T cells into unique tissue-resident subsets gives the host enhanced regional immunity. In recent years, there has been considerable progress in our understanding of tissue-resident T cell development and function, revealing mechanisms for enhanced protective immunity that have the potential to influence rational vaccine design. This Review discusses the major advances and the emerging concepts in this field, summarizes what is known about the differentiation and the protective functions of tissue-resident memory T cells in different tissues in the body and highlights key unanswered questions.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-24 — faithfulness

**Claim:** The latent infection of myeloid cells with human cytomegalovirus induces a number of changes in gene expression.

**Answer sentences:**

1. Yes, the latent infection of myeloid cells with human cytomegalovirus induces changes in gene expression, as evidenced by the detection of specific viral transcripts during latency, such as the UL111.5A-region transcript [26133404].
2. Additionally, the expression of viral interleukin-10 (vIL-10) during latency has been shown to modulate the differentiation of latently infected myeloid progenitors [26873988].
3. These findings highlight the impact of HCMV latency on gene expression in myeloid cells [26133404, 26873988].

**Cited abstracts:**

> **[26133404] A novel viral transcript with homology to human interleukin-10 is expressed during latent human cytomegalovirus infection.**
>
> Human cytomegalovirus (CMV) establishes latent infections in hematopoietic cells such as granulocyte-macrophage progenitors (GM-Ps). During latency the virus is sequestered in a nonreplicating state, although limited transcriptional activity has been previously reported. In this study we sought to further examine viral gene expression during the latent phase of infection. Using an experimental model of latency, primary human GM-Ps were latently infected with CMV strain Toledo and extracted RNA subjected to reverse transcription-PCR by using CMV gene-specific primers. Using this approach, we detected transcription from the UL111.5A region of the viral genome. This transcription was also detected in GM-Ps latently infected with AD169 and Towne strains, indicating that expression was CMV strain independent. Significantly, we detected UL111.5A-region transcripts in mononuclear cells from healthy bone marrow and mobilized peripheral blood allograft donors, demonstrating expression during natural latent infection. Mapping experiments with RNA extracted from latently infected GM-Ps revealed the expression of a novel UL111.5A region transcript with a splicing pattern that differed from that reported during productive infection of permissive cells. This UL111.5A region transcript expressed during latent infection is predicted to encode a 139-amino-acid protein with homology to the potent immunosuppressor interleukin-10 (IL-10) and to the viral IL-10 homolog that is expressed during productive CMV infection. Expression of a latency-associated cmvIL-10 may confer upon the virus an ability to avoid immune recognition and clearance during the latent phase of infection.

> **[26873988] Viral interleukin-10 expressed by human cytomegalovirus during the latent phase of infection modulates latently infected myeloid cell differentiation.**
>
> The human cytomegalovirus UL111A gene is expressed during latent and productive infections, and it codes for homologs of interleukin-10 (IL-10). We examined whether viral IL-10 expressed during latency altered differentiation of latently infected myeloid progenitors. In comparison to infection with parental virus or mock infection, latent infection with a virus in which the gene encoding viral IL-10 has been deleted upregulated cytokines associated with dendritic cell (DC) formation and increased the proportion of myeloid DCs. These data demonstrate that viral IL-10 restricts the ability of latently infected myeloid progenitors to differentiate into DCs and identifies an immunomodulatory role for viral IL-10 which may limit the host's ability to clear latent virus.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-25 — abstention

**Claim:** Transcription rates in S. cerevisiae range between 7 and 12 kb/min.

**Answer:** NOT_FOUND

**All retrieved abstracts:**

> **[16237005] Single-RNA counting reveals alternative modes of gene expression in yeast**
>
> Proper execution of transcriptional programs is a key requirement of gene expression regulation, demanding accurate control of timing and amplitude. How precisely the transcription machinery fulfills this task is not known. Using an in situ hybridization approach that detects single mRNA molecules, we measured mRNA abundance and transcriptional activity within single Saccharomyces cerevisiae cells. We found that expression levels for particular genes are higher than initially reported and can vary substantially among cells. However, variability for most constitutively expressed genes is unexpectedly small. Combining single-transcript measurements with computational modeling indicates that low expression variation is achieved by transcribing genes using single transcription-initiation events that are clearly separated in time, rather than by transcriptional bursts. In contrast, PDR5, a gene regulated by the transcription coactivator complex SAGA, is expressed using transcription bursts, resulting in larger variation. These data directly demonstrate the existence of multiple expression modes used to modulate the transcriptome.

> **[365896] RiboSys, a high-resolution, quantitative approach to measure the in vivo kinetics of pre-mRNA splicing and 3'-end processing in Saccharomyces cerevisiae.**
>
> We describe methods for obtaining a quantitative description of RNA processing at high resolution in budding yeast. As a model gene expression system, we constructed tetON (for induction studies) and tetOFF (for repression, derepression, and RNA degradation studies) yeast strains with a series of reporter genes integrated in the genome under the control of a tetO7 promoter. Reverse transcription and quantitative real-time-PCR (RT-qPCR) methods were adapted to allow the determination of mRNA abundance as the average number of copies per cell in a population. Fluorescence in situ hybridization (FISH) measurements of transcript numbers in individual cells validated the RT-qPCR approach for the average copy-number determination despite the broad distribution of transcript levels within a population of cells. In addition, RT-qPCR was used to distinguish the products of the different steps in splicing of the reporter transcripts, and methods were developed to map and quantify 3'-end cleavage and polyadenylation. This system permits pre-mRNA production, splicing, 3'-end maturation and degradation to be quantitatively monitored with unprecedented kinetic detail, suitable for mathematical modeling. Using this approach, we demonstrate that reporter transcripts are spliced prior to their 3'-end cleavage and polyadenylation, that is, cotranscriptionally.

> **[36606083] Quantitative, genome-wide analysis of eukaryotic replication initiation and termination.**
>
> Many fundamental aspects of DNA replication, such as the exact locations where DNA synthesis is initiated and terminated, how frequently origins are used, and how fork progression is influenced by transcription, are poorly understood. Via the deep sequencing of Okazaki fragments, we comprehensively document replication fork directionality throughout the S. cerevisiae genome, which permits the systematic analysis of initiation, origin efficiency, fork progression, and termination. We show that leading-strand initiation preferentially occurs within a nucleosome-free region at replication origins. Using a strain in which late origins can be induced to fire early, we show that replication termination is a largely passive phenomenon that does not rely on cis-acting sequences or replication fork pausing. The replication profile is predominantly determined by the kinetics of origin firing, allowing us to reconstruct chromosome-wide timing profiles from an asynchronous culture.

> **[2817000] Histone Variant H2A.Z Marks the 5′ Ends of Both Active and Inactive Genes in Euchromatin**
>
> In S. cerevisiae, histone variant H2A.Z is deposited in euchromatin at the flanks of silent heterochromatin to prevent its ectopic spread. We show that H2A.Z nucleosomes are found at promoter regions of nearly all genes in euchromatin. They generally occur as two positioned nucleosomes that flank a nucleosome-free region (NFR) that contains the transcription start site. Astonishingly, enrichment at 5' ends is observed not only at actively transcribed genes but also at inactive loci. Mutagenesis of a typical promoter revealed a 22 bp segment of DNA sufficient to program formation of a NFR flanked by two H2A.Z nucleosomes. This segment contains a binding site of the Myb-related protein Reb1 and an adjacent dT:dA tract. Efficient deposition of H2A.Z is further promoted by a specific pattern of histone H3 and H4 tail acetylation and the bromodomain protein Bdf1, a component of the Swr1 remodeling complex that deposits H2A.Z.

> **[84580585] Guide to yeast genetics and molecular biology**
>
> This volume and its companion, Volume 350, are specifically designed to meet the needs of graduate students and postdoctoral students as well as researchers, by providing all the up-to-date methods necessary to study genes in yeast. Procedures are included that enable newcomers to set up a yeast laboratory and to master basic manipulations. Relevant background and reference information given for procedures can be used as a guide to developing protocols in a number of disciplines. Specific topics addressed in this book include cytology, biochemistry, cell fractionation, and cell biology.

*Question: justified? (yes = no abstract reports anything about the claim)*

## v2-26 — faithfulness

**Claim:** A diminished ovarian reserve does not solely indicate infertility in an a priori non-infertile population.

**Answer sentences:**

1. The study found that among women aged 30 to 44 years without a history of infertility, biomarkers indicating diminished ovarian reserve were not associated with reduced fertility [13497630].
2. This suggests that a diminished ovarian reserve does not solely indicate infertility in this population.
3. The findings do not support the use of these biomarkers to assess natural fertility for women with these characteristics [13497630].
4. No other abstracts address this specific claim.

**Cited abstracts:**

> **[13497630] Association Between Biomarkers of Ovarian Reserve and Infertility Among Older Women of Reproductive Age**
>
> Importance Despite lack of evidence of their utility, biomarkers of ovarian reserve are being promoted as potential markers of reproductive potential. Objective To determine the associations between biomarkers of ovarian reserve and reproductive potential among women of late reproductive age. Design, Setting, and Participants Prospective time-to-pregnancy cohort study (2008 to date of last follow-up in March 2016) of women (N = 981) aged 30 to 44 years without a history of infertility who had been trying to conceive for 3 months or less, recruited from the community in the Raleigh-Durham, North Carolina, area. Exposures Early-follicular-phase serum level of antimüllerian hormone (AMH), follicle-stimulating hormone (FSH), and inhibin B and urinary level of FSH. Main Outcomes and Measures The primary outcomes were the cumulative probability of conception by 6 and 12 cycles of attempt and relative fecundability (probability of conception in a given menstrual cycle). Conception was defined as a positive pregnancy test result. Results A total of 750 women (mean age, 33.3 [SD, 3.2] years; 77% white; 36% overweight or obese) provided a blood and urine sample and were included in the analysis. After adjusting for age, body mass index, race, current smoking status, and recent hormonal contraceptive use, women with low AMH values (<0.7 ng/mL [n = 84]) did not have a significantly different predicted probability of conceiving by 6 cycles of attempt (65%; 95% CI, 50%-75%) compared with women (n = 579) with normal values (62%; 95% CI, 57%-66%) or by 12 cycles of attempt (84% [95% CI, 70%-91%] vs 75% [95% CI, 70%-79%], respectively). Women with high serum FSH values (>10 mIU/mL [n = 83]) did not have a significantly different predicted probability of conceiving after 6 cycles of attempt (63%; 95% CI, 50%-73%) compared with women (n = 654) with normal values (62%; 95% CI, 57%-66%) or after 12 cycles of attempt (82% [95% CI, 70%-89%] vs 75% [95% CI, 70%-78%], respectively). Women with high urinary FSH values (>11.5 mIU/mg creatinine [n = 69]) did not have a significantly different predicted probability of conceiving after 6 cycles of attempt (61%; 95% CI, 46%-74%) compared with women (n = 660) with normal values (62%; 95% CI, 58%-66%) or after 12 cycles of attempt (70% [95% CI, 54%-80%] vs 76% [95% CI, 72%-80%], respectively). Inhibin B levels (n = 737) were not associated with the probability of conceiving in a given cycle (hazard ratio per 1-pg/mL increase, 0.999; 95% CI, 0.997-1.001). Conclusions and Relevance Among women aged 30 to 44 years without a history of infertility who had been trying to conceive for 3 months or less, biomarkers indicating diminished ovarian reserve compared with normal ovarian reserve were not associated with reduced fertility. These findings do not support the use of urinary or blood follicle-stimulating hormone tests or antimüllerian hormone levels to assess natural fertility for women with these characteristics.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-27 — faithfulness

**Claim:** G-CSF increases the expansion and infiltration of MDSCs into tumors.

**Answer sentences:**

1. G-CSF increases the expansion and infiltration of MDSCs into tumors, as demonstrated by studies showing that tumor-initiating cells exhibit elevated G-CSF, which promotes MDSC accumulation [2014909].

**Cited abstracts:**

> **[2014909] Oncogenic mTOR signaling recruits myeloid-derived suppressor cells to promote tumor initiation**
>
> Myeloid-derived suppressor cells (MDSCs) play critical roles in primary and metastatic cancer progression. MDSC regulation is widely variable even among patients harbouring the same type of malignancy, and the mechanisms governing such heterogeneity are largely unknown. Here, integrating human tumour genomics and syngeneic mammary tumour models, we demonstrate that mTOR signalling in cancer cells dictates a mammary tumour's ability to stimulate MDSC accumulation through regulating G-CSF. Inhibiting this pathway or its activators (for example, FGFR) impairs tumour progression, which is partially rescued by restoring MDSCs or G-CSF. Tumour-initiating cells (TICs) exhibit elevated G-CSF. MDSCs reciprocally increase TIC frequency through activating Notch in tumour cells, forming a feedforward loop. Analyses of primary breast cancers and patient-derived xenografts corroborate these mechanisms in patients. These findings establish a non-canonical oncogenic role of mTOR signalling in recruiting pro-tumorigenic MDSCs and show how defined cancer subsets may evolve to promote and depend on a distinct immune microenvironment.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-28 — faithfulness

**Claim:** Diabetes remission occurs more in people treated with conventional therapy than in people treated with laparoscopic adjustable gastric banding surgery.

**Answer sentences:**

1. Diabetes remission occurs more in people treated with laparoscopic adjustable gastric banding surgery than in people treated with conventional therapy.
2. In a randomized controlled trial, remission of type 2 diabetes was achieved by 73% in the surgical group and 13% in the conventional-therapy group [7098463].

**Cited abstracts:**

> **[7098463] Adjustable gastric banding and conventional therapy for type 2 diabetes: a randomized controlled trial.**
>
> CONTEXT Observational studies suggest that surgically induced loss of weight may be effective therapy for type 2 diabetes. OBJECTIVE To determine if surgically induced weight loss results in better glycemic control and less need for diabetes medications than conventional approaches to weight loss and diabetes control. DESIGN, SETTING, AND PARTICIPANTS Unblinded randomized controlled trial conducted from December 2002 through December 2006 at the University Obesity Research Center in Australia, with general community recruitment to established treatment programs. Participants were 60 obese patients (BMI >30 and <40) with recently diagnosed (<2 years) type 2 diabetes. INTERVENTIONS Conventional diabetes therapy with a focus on weight loss by lifestyle change vs laparoscopic adjustable gastric banding with conventional diabetes care. MAIN OUTCOME MEASURES Remission of type 2 diabetes (fasting glucose level <126 mg/dL [7.0 mmol/L] and glycated hemoglobin [HbA1c] value <6.2% while taking no glycemic therapy). Secondary measures included weight and components of the metabolic syndrome. Analysis was by intention-to-treat. RESULTS Of the 60 patients enrolled, 55 (92%) completed the 2-year follow-up. Remission of type 2 diabetes was achieved by 22 (73%) in the surgical group and 4 (13%) in the conventional-therapy group. Relative risk of remission for the surgical group was 5.5 (95% confidence interval, 2.2-14.0). Surgical and conventional-therapy groups lost a mean (SD) of 20.7% (8.6%) and 1.7% (5.2%) of weight, respectively, at 2 years (P < .001). Remission of type 2 diabetes was related to weight loss (R2 = 0.46, P < .001) and lower baseline HbA1c levels (combined R2 = 0.52, P < .001). There were no serious complications in either group. CONCLUSIONS Participants randomized to surgical therapy were more likely to achieve remission of type 2 diabetes through greater weight loss. These results need to be confirmed in a larger, more diverse population and have long-term efficacy assessed. TRIAL REGISTRATION actr.org Identifier: ACTRN012605000159651.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-29 — faithfulness

**Claim:** Gpr124 increases BBB breakdown in mouse models of ischemic stroke.

**Answer sentences:**

1. Yes, Gpr124 increases BBB breakdown in mouse models of ischemic stroke, as evidenced by the study showing that Gpr124 conditional knockout (CKO) in the endothelia of adult mice resulted in BBB disruption and microvascular hemorrhage in mouse models of ischemic stroke [6325527].

**Cited abstracts:**

> **[6325527] Gpr124 is essential for blood–brain barrier integrity in central nervous system disease**
>
> Although blood–brain barrier (BBB) compromise is central to the etiology of diverse central nervous system (CNS) disorders, endothelial receptor proteins that control BBB function are poorly defined. The endothelial G-protein-coupled receptor (GPCR) Gpr124 has been reported to be required for normal forebrain angiogenesis and BBB function in mouse embryos, but the role of this receptor in adult animals is unknown. Here Gpr124 conditional knockout (CKO) in the endothelia of adult mice did not affect homeostatic BBB integrity, but resulted in BBB disruption and microvascular hemorrhage in mouse models of both ischemic stroke and glioblastoma, accompanied by reduced cerebrovascular canonical Wnt–β-catenin signaling. Constitutive activation of Wnt–β-catenin signaling fully corrected the BBB disruption and hemorrhage defects of Gpr124-CKO mice, with rescue of the endothelial gene tight junction, pericyte coverage and extracellular-matrix deficits. We thus identify Gpr124 as an endothelial GPCR specifically required for endothelial Wnt signaling and BBB integrity under pathological conditions in adult mice. This finding implicates Gpr124 as a potential therapeutic target for human CNS disorders characterized by BBB disruption.

*Question: faithful? (yes = every sentence SUPPORTED)*

## v2-30 — faithfulness

**Claim:** Immune responses in immune cells are geographically segregated.

**Answer sentences:**

1. Immune responses in immune cells can be geographically segregated, as evidenced by the formation of localized cytokine niches with sharp boundaries, which contribute to cell-to-cell variability [4928282].
2. Additionally, tissue-resident memory T cells are specialized for regional immunity, indicating a degree of geographic segregation in immune responses [3155731].
3. These findings support the idea that immune responses are not uniformly distributed but are instead localized to specific areas.

**Cited abstracts:**

> **[4928282] A Tunable Diffusion‐Consumption Mechanism of Cytokine Propagation Enables Plasticity in Cell‐to‐Cell Communication in the Immune System**
>
> &NA; Immune cells communicate by exchanging cytokines to achieve a context‐appropriate response, but the distances over which such communication happens are not known. Here, we used theoretical considerations and experimental models of immune responses in vitro and in vivo to quantify the spatial extent of cytokine communications in dense tissues. We established that competition between cytokine diffusion and consumption generated spatial niches of high cytokine concentrations with sharp boundaries. The size of these self‐assembled niches scaled with the density of cytokine‐consuming cells, a parameter that gets tuned during immune responses. In vivo, we measured interactions on length scales of 80–120 &mgr;m, which resulted in a high degree of cell‐to‐cell variance in cytokine exposure. Such heterogeneous distributions of cytokines were a source of non‐genetic cell‐to‐cell variability that is often overlooked in single‐cell studies. Our findings thus provide a basis for understanding variability in the patterning of immune responses by diffusible factors. Graphical Abstract Figure. No caption available. HighlightsCytokine penetration in tissues is governed by a diffusion‐consumption mechanismSpherical cytokine niches are generated around cytokine‐producing cellsThe characteristic niche size depends on the density of cytokine consumersCytokine niches are a source of variability in otherwise identical cells &NA; Cytokine‐mediated communication allows immune cells to achieve a context‐appropriate response, but the distance over which this communication happens is unclear. Oyler‐Yaniv et al. (2017) show that a simple diffusion‐consumption mechanism quantitatively describes the spatial spread of cytokines in vivo and results in localized niches of high cytokine concentrations that contribute to cell‐to‐cell variability.

> **[3155731] Tissue-resident memory T cells: local specialists in immune defence**
>
> T cells have crucial roles in protection against infection and cancer. Although the trafficking of memory T cells around the body is integral to their capacity to provide immune protection, studies have shown that specialization of some memory T cells into unique tissue-resident subsets gives the host enhanced regional immunity. In recent years, there has been considerable progress in our understanding of tissue-resident T cell development and function, revealing mechanisms for enhanced protective immunity that have the potential to influence rational vaccine design. This Review discusses the major advances and the emerging concepts in this field, summarizes what is known about the differentiation and the protective functions of tissue-resident memory T cells in different tissues in the body and highlights key unanswered questions.

*Question: faithful? (yes = every sentence SUPPORTED)*
