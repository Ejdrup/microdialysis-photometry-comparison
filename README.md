# microdialysis-photometry-comparison
Repository for data and code associated with the manuscript *Within-animal comparison of dopamine measured with microdialysis and fiber photometry in amphetamine-exposed mice*.


All data is stored within the *data* folder under either *fiber photometry* or *microdialysis*. A Spyder notebook with Python code is supplied to pre-process the fiber photometry data as detailed in the method section of the manuscript. The same script also convert the microdialysis data (fmol/uL) to fold change over baseline. Finally, both outputs can be plotted with the last two sections of the Spyder notebook.


The *fiber photometry* folder contains a .txt file for each of the 14 mice, 7 of whom received amphetamine and 7 vehicle injection.
The files are 2xN in size, with row 1 containing the 415 nm isosbestic channel and and row 2 the 470 nm signal channel. They are sampled at 20 Hz, and injection is given at the 80,000th index, except for one session (two mice), where the recording broke down early on and was restarted. These two mice are injected at index 55,000. This is detailed in the Python scipt as well.


The *microdialysis* folder contains one .txt file for amphetine-injected mice and one for vehicle-injected mice. These are stored in a 10x7 format, with each column a different mouse and each row a time point. The samples are interspaced with 20 minutes and starts 80 minutes before injection.



