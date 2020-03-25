# FaceLens

This application can be used as a system tool to sort multiple images into separate folders based on the person/s present in it.


**To Create your own dataset :**
1) Place some images in the Raw folder (or edit the paths.py file).
2) Run extract_faces.py to separate faces from these images. These will be saved in the Faces folder.
3) Now manually separate the faces into their respective folder (having corresponding foldername) and keep them in the Dataset folder.
4) Now run create_dataset.py and call its processFaces() function, to create the pickle file (dataset.pkl). 

**To Measure the performance :**
1) Uncomment one of the import statements of measure_performance.py file to select the algorithm to be assessed.
2) Now run measure_performance.py to calculate the accuracy and construction of confusion matrix.

**To Recognize faces in an image :**
1) Run recognizeFacesInImage() function of recognize_faces.py, and pass it the path to the image file. For using compare faces method.
2) OR Run recognizeFacesInImage() function of knn_train.py (along with file path) for K-Nearest Neighbor algorithm.
3) OR Run recognizeFacesInImage() function of svm_train.py (along with file path) for Support Vector Machine algorithm.

**To Sort images in a folder based on faces (without UI) :**
1) Open sort_files and uncomment last 3 lines of the code.
2) Set sortingOrder as per requirements.
3) Set the path of the folder to work on 
4) Set whether or not to allow multiple copying of images.
5) Run sort_files.py to start the sorting process.

**To Sort images in a folder based on faces (with UI) :**
1) Make sure last 3 statements are commented in sort_files.py
2) Run main.py with followig command :
	python3 main.py path/to/folder/
