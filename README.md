HSSA — *Hyperspectral Segmentation Algorithm*
=============================================

Conception
----------

The <span style="font-variant:small-caps;">hssa</span> is a two-staged
segmentation tool for <span style="font-variant:small-caps;">hs</span>
images. It is based on consecutive division of image to decompose it into a set of homogenous segments. Later, according to labels assigned by an expert, the representation is prepared as an input for classification methods.

The method was inspired by the *quad trees* @mango, which are a class of
hierarchical data structures, based on regular decomposition. The base
image is decomposed here by splitting it by each spatial dimension into
four non-overlapping subregions of equal size, repetitively, until
sub-images became homogenous. As the result, the image is saved in a
tree structure, where every leaf refers to one homogenous region of the
original image. The process is depicted in Figure below.

![Decomposition of image region using *quad tree* @banana.<span
data-label="fig:hssa_quadtrees"></span>](figures/hssa_quadtrees.png)

![Decomposition of image region using *quad tree* @banana.<span
data-label="fig:hssa_quadtrees"></span>](figures/quad_tree.png)

In a contrast to *quad trees*, <span
style="font-variant:small-caps;">hssa</span> uses *frame lists* instead
of a tree structure. It additionally introduces a novel homogeneity
measure. In final stage, the proposed segmentation procedure merges
similar frames into larger homogeneous segments.

Construction
------------

### Main loop

Algorithm identifies the most representative homogenous regions of the
given picture, which are represented as frames encoded in the form of
vectors consisting of two parts:

-   The set of the parameters used by <span
    style="font-variant:small-caps;">hssa</span>
    (Table below).

-   Mean signature of the pixels inside the frame.


 
| col. | parameter| description|
|---|---|---|
|1|`fold`|Number of iteration in which segment was created|
|2|`frame_id`|      Unique identifier
|3|`segment_id`|    Identifier of group of segments resulting from merging procedure
|4|`class_label`|   Class label given by expert for region
|5|`homogeneity`|   Homogeneity measure


Procedure uses two sets of frames:

-   **Homogenous** — representative vectors of frames identified
    as homogenous.

-   **Heterogeneous** — all remaining frames.

The frame representation and declaration of those two structures are
enough to create pseudocode of <span
style="font-variant:small-caps;">hssa</span>, presented in Algorithm
\[alg:hssa\].

\[!ht\]

\[1\] $heterogenous\gets image$\[alg:hssa\_init\] $homogenous\gets [\;]$
$frame.signature = mean(frame)$\[alg:hssa\_mean\_calc\]
$frame.homogeneity = homogeneity(frame)$\[alg:hssa\_homo\_calc\]
\[alg:hssa\_threshold\] $homogenous\gets homogenous + frame$
$heterogenous\gets heterogenous - frame$ \[alg:hssa\_end\] **break**
$split(frame)$\[alg:hssa\_divide\]

The algorithm receives the following input parameters:

-   $image$ — *hyperspectral* image data,

-   $threshold$ — lowest acceptable value of homogeneity which is used
    for determining homogenous regions.

-   $maxFold$ — maximum number of loops,

The initialization procedure creates a single frame for the entire
image, and its representative vector is added to the heterogeneous list
(line \[alg:hssa\_init\]). Every iteration calculates the mean signature
(line \[alg:hssa\_mean\_calc\]) and homogeneity measure (line
\[alg:hssa\_homo\_calc\]) for all frames in *heterogeneous* list. If the
measure of the given frame reaches $threshold$ (line
\[alg:hssa\_threshold\]), it is assessed as homogeneous and moved to the
*homogeneous* list. The end of a main loop divides *heterogenous* frames
into smaller ones (line \[alg:hssa\_divide\]).

Procedure breaks when any of the following statements is satisfied:

-   *heterogeneous* list becomes empty (line \[alg:hssa\_end\]),

-   number of proceeded loops exceeds the $maxFold$.

Areas covered by *homogeneous* (black) and *heterogeneous* (white)
frames for *Salinas* dataset, according to loop iterations are presented
in Figure \[fig:hssa\_segmentation\].

![<span style="font-variant:small-caps;">hssa</span> segmentation
process. Black areas present *homogenous* frames.<span
data-label="fig:hssa_segmentation"></span>](hssa_segmentation_5){width="\textwidth"}

### Homogeneity measure

It is easy to to establish a measure of *homogeneity* for binary images.
Frames in this kind of data are homogenous if every pixel inside shares
the same value. Nevertheless for more complex pictures (and the<span
style="font-variant:small-caps;">hs</span> images definitely belongs to
this class) it is necessary to provide accordingly more complex method
to calculate this property (Algorithm \[alg:hssa\_homogeneity\]).

\[!ht\]

\[1\]
$meanSignature\gets mean(frame.pixels)$\[alg:hssa\_homogeneity\_1\]
$bubbles\gets [\;]$ $x'\gets x * frame.width / 3$
$y'\gets y * frame.height / 3$\[alg:hssa\_homogeneity\_2\]
$accumulator\gets [\;]$
$accumulator\gets accumulator + frame.pixels[x'+x'',y'+y'']$\[alg:hssa\_homogeneity\_3\]
$bubble \gets mean(accumulator)$ $bubbles\gets bubbles + bubble$
**return** $max(distance(bubbles, meanSignature))$
\[alg:hssa\_homogeneity\_4\]

Proposition is to:

-   Calculate the regions signature as the mean of all its pixel
    signatures (line \[alg:hssa\_homogeneity\_1\]).

-   Establish $3$x$3$ grid on the image, to select 4 pixels on each
    crossing of grid lines (line \[alg:hssa\_homogeneity\_2\]).

-   Calculate the average signature for nearest neighborhood (in the
    radius of 5 pixels, which is here called a bubble) of each selected
    pixel (line \[alg:hssa\_homogeneity\_3\]).

-   The largest euclidean distance between mean signature of whole frame
    and four bubbles is returned as the homogeneity measure
    (line \[alg:hssa\_homogeneity\_4\]).

Threshold of homogeneity should be provided by the user by tuning it to
the specific problem. For all later experiments, this parameter was set
to 98%.

### Merging homogenous frames to segments

The product of <span style="font-variant:small-caps;">hssa</span>
procedure is a set of *homogeneous* frames. Preliminary tests showed
that plenty of them, accordingly to their signatures, could be grouped
to equally homogenous subsets. Therefore, the algorithm ends with a
procedure of merging similar *frames* into larger *segments*. It brings
the essential advantage by reducing the engagement of the human expert
in the labelling process, where it is enough to label a relatively small
collection of segments instead of significantly larger set of frames.

In order to calculate a similarity between the frames, a simple
Euclidean distance between their signatures is used. Similar frames
receive the same `segment_id` and require only one expertise labelling
decision.

However, being aware of the fact that reducing a number of segments
leads to significant reduction of a number of samples used in the
training procedure could lead to decrease classification, suggested to
develop three versions of the segment representations:

1.  *Single Representative Signature* (<span
    style="font-variant:small-caps;">srs</span>) — *one* signature for
    *each* segment, calculated by averaging the signatures of all frames
    which builds the segment.

2.  *All Regions Signature* (<span
    style="font-variant:small-caps;">ars</span>) — signatures of *all
    frames* in the segment.

3.  *Pixels Signature* (<span
    style="font-variant:small-caps;">ps</span>) — signatures of *all
    pixels* which belong to the segment.

It should be emphasized, that *all propositions require the human expert
to label each segment only once*. The label assigned to a particular
segment is then propagated to all samples which belong to it.

### Implementation

The <span style="font-variant:small-caps;">hssa</span> was implemented
as a script in the pure <span
style="font-variant:small-caps;">matlab</span> language, without usage
of any additional *toolboxes*.

Its full code and documentation is available at
<https://github.com/w4k2/hssa>.
