# Progetto di Machine Learning e Sistemi Intelligenti per Internet  [ ML3-Educational-YouTube-Video-Classifier]

Identificazione (classificazione) di materiale multimediale (es. Video Youtube, PDF) adatto a corsi didattici online con tecniche di Computer Vision e Deep Learning.

Di seguito sono elencate e descritte brevemente le features relativi ai viedeo ed audio identificate e calcolate per i video del dataset. 

## Aesthetic-visual Features

* **Brightness** - Rappresenta la luminosità media del video.
* **Entropy** - Per misurare se un'immagine non è interessante o vivace, calcoleremo l'entropia dell'intensità dei pixel presenti nell'immagine. Saremo in grado di distinguere un'immagine come poco interessante se ha poca o nessuna variazione nella sua intensità di pixel e bassa entropia, in contrasto con un'immagine vivace che ha molti valori di intensità di pixel diversi e un'alta entropia.
* **Text Density** - Il rapporto medio tra la dimensione totale dell’immagine e le aree (blocks) di testo del frame. Per alcune tipologie di video didattici questa feature avrà un valore molto alto (per esempio, video puramente con slides o con lavagne).
* **Subjet Mask** - La regione del soggetto tende ad avere una salienza più alta rispetto allo sfondo, il che significa che le mappe di salienza possono essere utilizzate per prevedere il soggetto e lo sfondo corrispondenti ai pixel dell'immagine.
* **Subject Contrast** - L'illuminazione del soggetto e dello sfondo forniscono un contrasto importante. Si evidenzia l'importanza di avere una notevole distinzione nella luminosità tra soggetto e sfondo. Nella sua ricerca, le immagini più esteticamente piacevoli sono quelle con un alto contrasto soggetto / sfondo.
* **Background Color Simplicity** - Quando si considerano gli sfondi nelle immagini, è importante tenere conto della distribuzione del colore. Questa funzione valuta l'area di sfondo per ottenere la sua semplicità di colore. Le immagini che presentano uno sfondo con un'elevata complessità cromatica concentreranno un'elevata attenzione, distraendo così l'osservatore dal soggetto che l'immagine intende evidenziare.

## Audio Features

* **Voice frequencies** - Ampiezza media delle frequenze della voce umana.
* **Non voice frequencies** - Ampiezza media delle frequenze non vocali.
* **Mel-frequency cepstral coefficients (MFCC)** - Rappresentano caratteristiche timbriche di un file audio. Gli MFCC si sono dimostrati utili per molte attività di elaborazione audio e musicale. Forniscono una rappresentazione compatta dell'inviluppo spettrale e sono anche una rappresentazione musicalmente significativa e sono usati per catturare scene acustiche.
* **RelevantWordsCount** - Rappresenta la quantià di parole di tipo didattico presenti in un video

## Classificazione

Di seguito è riportato il grafico riportante al percentuale di accuratezza della rete neurale per il classficato realizzato.

![alt text](https://github.com/GiuliaSim/ML3-Educational-YouTube-Video-Classifier/blob/master/piePlot_1.png)
