from kd_tree import Node
from kd_tree import KDTree

import minutiae as minut
import os

def main():
    there_similarity = False
    image_path = input("Enter the image path: ")
    dataset_path = input("Enter the dataset path: ")
    minutiae_image = minut.extract_minutiae(image_path)
    original_image = minut.cv2.imread(image_path)
    minutiae_tree = KDTree(minutiae_image,0)
    print("Showing the result that has similarity score above 50%")
    for filename in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, filename)
        if os.path.isfile(file_path):
            dataset_image = minut.extract_minutiae(file_path)
            dataset_tree = KDTree(dataset_image,0)
            matched_points = minut.match_fingerprints(minutiae_image,dataset_tree,2)
            num_matched = len(matched_points)
            similarity_score = (num_matched/len(minutiae_image))*100
            if (similarity_score >= 50):
                there_similarity = True
                print("File:",filename)
                print("Similarity Score:", similarity_score)
    if (not there_similarity):
        print("It seems that none of the datasets has similarity score above 50% when compared to the query!")        

if __name__ == "__main__":
    main()