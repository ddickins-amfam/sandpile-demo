presentation_start = r"""
    \documentclass{beamer}

    \usepackage[utf8]{inputenc}
    \usepackage{graphicx}
    %\usepackage{amsmath}
    \graphicspath{ {./images/} }
    \usepackage{subcaption}

    \usepackage{enumitem}
    \setlist{itemsep=10pt}
    \setitemize{label=\usebeamerfont*{itemize item}%
      \usebeamercolor[fg]{itemize item}
      \usebeamertemplate{itemize item}}

    %Information to be included in the title page:
    \title{Stabilization Flipbook}
    %\author{Anonymous}
    %\institute{ShareLaTeX}
    \date{2018}

    \begin{document}
    \frame{\titlepage}
    """


presentation_insert = r"""
    \begin{frame}
      \begin{figure}[h!]
        \centering
          \includegraphics[scale=0.25]{sandpile_%i}
      \end{figure}
    \end{frame}
    """

presentation_history = r"""
    \begin{frame}

    %s

    \[
    \{%s\}
    \]
    \end{frame}
    """

presentation_end = r"""
    \end{document}
    """
