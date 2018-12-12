# Creating a workflow

In bioinformatics, a pipeline is defined as a sequence of bioinformatics tools that transform and analyze the input data. 
A pipeline in CloudConductor is representes as a directed graph of modules, where a module is a bioinformatics tool.
Consider **Figure 1** as an example of a pipeline.

<figure align="center">
    <img src="../_static/Figure1.png" alt="An example of a pipeline" />
    <figcaption><b>Figure 1.</b> An example of a pipeline</figcaption>
</figure>

Before we explain how to define a pipeline, let's first describe how to define a module in a pipeline.

## Modules

A module is a bioinformatics tool and a submodule is a function that a bioinformatics tool is performing.
Some bioinformatics tools have only one function, thus their modules have only one submodule.
In **Figure 1**, `Samtools` is a module with two submodules: `Index` and `Flagstat`, while `BWA` is one module with one submodule with the same name.
Modules and submodules are predefined. [Here](#available-modules) is a list of currently available modules and submodules.
Please read the advanced topics if you would like to define your own modules and submodules

In a pipeline, a pipeline step is defined using the keywords ***module*** and ***submodule*** as following:

    [*unique_name_of_pipeline_step*]
        module=*name_of_module*
        submodule=*name_of_submodule_used*

Each submodule is defined by a set of *input keys*, *output keys* and a *command*. 
The submodule is running the *command* on the *input keys* and generates output as *output_keys*.
In **Figure 1**, submodule `Index` from module `Samtools` has 
one input key ("*bam*" - the input BAM file) and one output key ("*bam_idx*" - the output BAM index file).

You can specify to keep an output file generated by a module using the keyword ***final_output*** in the module definition. 
For example, if you want to keep the indexed file after running `samtools index` you would define the module as following:

    [bam_indexing]
        module=Samtools
        submodule=Index
        final_output=bam_idx

Additionally, using the keyword ***docker_image*** you are able to specify which Docker image from resource kit you want CloudConductor to use.
If no ***docker_image*** is specified, then the tool executable is obtain from the external resources list from resource kit.

More information about resources and Docker will be presented in the definition of the resource kit.

## Create a pipeline graph

To create a pipeline graph, you need to connect the modules using the keyword ***input_from***.
For example, in **Figure 1**, BWA receives the *input from* Trimmomatic.

The value of an ***input_from*** key is a set of defined unique *pipeline steps*.
The pipeline presented in **Figure 1** can be represented as following:

    [trim_reads]
        module=Trimmomatic
        docker_image=Trimmomatic_docker

    [align_reads]
        module=BWA
        input_from=trim_reads
        final_output=bam

    [bam_indexing]
        module=Samtools
        submodule=Index
        docker_image=Samtools_docker
        input_from=align_reads
        final_output=bam_idx

    [bam_summary]
        module=Samtools
        submodule=Flagstat
        docker_image=Samtools_docker
        input_from=align_reads
        final_output=flagstat

As you can observe, there is no need to specify the submodules for `Trimmomatic` or `BWA` as they have only one submodule with the same name.
Also, we decided to not keep the output of Trimmomatic, but you can always add *fastq* as ***final_output*** to keep it.

## Available modules

Here is a list of currently implemented modules and their submodules:

<table style="width:100%;" border=1>
    <tr>
        <th> Type </th>
        <th> Module </th>
        <th> Submodule </th>
    </tr>
    <tr>
        <td rowspan=60> Tool (Module) </td>
        <td> Annovar </td>
        <td> Annovar </td>
    </tr>
    <tr>
        <td rowspan=2> Bcftools</td>
        <td> BcftoolsIndex</td>
    </tr>
    <tr>
        <td> BcftoolsNorm </td>
    </tr>
    <tr>
        <td> Bowtie2 </td>
        <td> Bowtie2 </td>
    </tr>
    <tr>
        <td> BwaAligner </td>
        <td> BwaAligner </td>
    </tr>
    <tr>
        <td> CellRanger </td>
        <td> CellRanger </td>
    </tr>
    <tr>
        <td> CNVkit </td>
        <td> CNVkit </td>
    </tr>
    <tr>
        <td> Cufflinks </td>
        <td> Cuffquant </td>
    </tr>
    <tr>
        <td> Cutadapt </td>
        <td> Cutadapt </td>
    </tr>
    <tr>
        <td> Delly </td>
        <td> Delly </td>
    </tr>
    <tr>
        <td rowspan=2> Diamond </td>
        <td> TaxonClassify </td>
    </tr>
    <tr>
        <td> BLASTX </td>
    </tr>
    <tr>
        <td> FastQC </td>
        <td> FastQC </td>
    </tr>
    <tr>
        <td rowspan=7> GATK </td>
        <td> HaplotypeCaller </td>
    </tr>
    <tr>
        <td> PrintReads </td>
    </tr>
    <tr>
        <td> BaseRecalibrator </td>
    </tr>
    <tr>
        <td> IndexVCF </td>
    </tr>
    <tr>
        <td> FilterMutectCalls </td>
    </tr>
    <tr>
        <td> CollectReadCounts </td>
    </tr>
    <tr>
        <td> BedToIntervalList </td>
    </tr>
    <tr>
        <td> Gistic2 </td>
        <td> Gistic2 </td>
    </tr>
    <tr>
        <td> Mosdepth </td>
        <td> Mosdepth </td>
    </tr>
    <tr>
        <td> NovoBreak </td>
        <td> NovoBreak </td>
    </tr>
    <tr>
        <td rowspan=4> Picard </td>
        <td> MarkDuplicates </td>
    </tr>
    <tr>
        <td> CollectInsertSizeMetrics </td>
    </tr>
    <tr>
        <td> SamToFastq </td>
    </tr>
    <tr>
        <td> SortGVCF </td>
    </tr>
    <tr>
        <td rowspan=10> QCParser </td>
        <td> FastQC </td>
    </tr>
    <tr>
        <td> PicardInsertSizeMetrics </td>
    </tr>
    <tr>
        <td> FastQC </td>
    </tr>
    <tr>
        <td> SamtoolsDepth </td>
    </tr>
    <tr>
        <td> SamtoolsFlagstat </td>
    </tr>
    <tr>
        <td> SamtoolsIdxstats </td>
    </tr>
    <tr>
        <td> Trimmomatic </td>
    </tr>
    <tr>
        <td> PrintTable </td>
    </tr>
    <tr>
        <td> MosdepthDist </td>
    </tr>
    <tr>
        <td> GATKCollectReadCount </td>
    </tr>
    <tr>
        <td rowspan=2> QCReportReader </td>
        <td> GetNumReadsFastQC </td>
    </tr>
    <tr>
        <td> GetNumReadsTrimmomatic </td>
    </tr>
    <tr>
        <td> RSEM </td>
        <td> RSEM </td>
    </tr>
    <tr>
        <td rowspan=5> Samtools </td>
        <td> Index </td>
    </tr>
    <tr>
        <td> Flagstat</td>
    </tr>
    <tr>
        <td> Idxstats </td>
    </tr>
    <tr>
        <td> View </td>
    </tr>
    <tr>
        <td> Depth </td>
    </tr>
    <tr>
        <td rowspan=3> SnpEff </td>
        <td> SnpEff </td>
    </tr>
    <tr>
        <td> SnpSiftAnnotate </td>
    </tr>
    <tr>
        <td> SnpSiftFilter </td>
    </tr>
    <tr>
        <td> Star </td>
        <td> Star </td>
    </tr>
    <tr>
        <td> Trimmomatic </td>
        <td> Trimmomatic </td>
    </tr>
    <tr>
        <td rowspan=10> Utils </td>
        <td> ConcatFastq </td>
    </tr>
    <tr>
        <td> RecodeVCF </td>
    </tr>
    <tr>
        <td> SummarizeVCF </td>
    </tr>
    <tr>
        <td> ViralFilter </td>
    </tr>
    <tr>
        <td> IndexVCF </td>
    </tr>
    <tr>
        <td> BGZip </td>
    </tr>
    <tr>
        <td> GetReadGroup </td>
    </tr>
    <tr>
        <td> CombineExpressionWithMetadata </td>
    </tr>
    <tr>
        <td> GetVCFChroms </td>
    </tr>
    <tr>
        <td> GetRefChroms </td>
    </tr>
    <tr>
        <td rowspan=6> Splitters </td>
        <td> BamSplitter </td>
        <td> BamSplitter </td>
    </tr>
    <tr>
        <td> FastqSplitter </td>
        <td> FastqSplitter </td>
    </tr>
    <tr>
        <td> RefSplitter </td>
        <td> RefSplitter </td>
    </tr>
    <tr>
        <td rowspan=2> SampleSplitter </td>
        <td> SampleSplitter </td>
    </tr>
    <tr>
        <td> TumorNormalSplitter </td>
    </tr>
    <tr>
        <td> VCFSplitter </td>
        <td> VCFSplitter </td>
    </tr>
    <tr>
        <td rowspan=20> Mergers </td>
        <td rowspan=2> CNVMergers </td>
        <td> MakeCNVPoN </td>
    </tr>
    <tr>
        <td> CNVkitExport </td>
    </tr>
    <tr>
        <td rowspan=3> Gatherers </td>
        <td> GatherBams </td>
    </tr>
    <tr>
        <td> GatherVCFs </td>
    </tr>
    <tr>
        <td> GatherGVCFs </td>
    </tr>
    <tr>
        <td rowspan=5> GATKMergers </td>
        <td> GenotypeGVCFs </td>
    </tr>
    <tr>
        <td> Mutect2 </td>
    </tr>
    <tr>
        <td> MergeBQSRs </td>
    </tr>
    <tr>
        <td> CatVariants </td>
    </tr>
    <tr>
        <td> CombineGVCF </td>
    </tr>
    <tr>
        <td> MergeBams </td>
        <td> MergeBams </td>
    </tr>
    <tr>
        <td rowspan=3> MergeRNAseq </td>
        <td> AggregateRawReadCounts </td>
    </tr>
    <tr>
        <td> AggreagateRSEMResults </td>
    </tr>
    <tr>
        <td> Cuffnorm </td>
    </tr>
    <tr>
        <td rowspan=2> QCReportMerger </td>
        <td> Rbind </td>
    </tr>
    <tr>
        <td> Cbind </td>
    </tr>
    <tr>
        <td rowspan=4> VCFMergers </td>
        <td> VCFMerger </td>
    </tr>
    <tr>
        <td> BGZipVCFMerger </td>
    </tr>
    <tr>
        <td> RecodedVCFMerger </td>
    </tr>
    <tr>
        <td> VCFSummaryMerger </td>
    </tr>
</table>