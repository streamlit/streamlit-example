import streamlit as st
import os
import cv2
from PIL import Image
import similarity_search
import tempfile
import pandas as pd
from gradio_client import Client
import json

# Path to the directory containing similar images
similar_images_dir = ".\gallery"

def read_image(image_file):
    img = cv2.imread(
        image_file, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
    )
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img is None:
        raise ValueError('Failed to read {}'.format(image_file))
    return img

def get_similar_images(image):
    # Process the uploaded image using the read_image function
    # processed_image = read_image(image)
    
    # Your similarity model logic here using the processed_image
    
    similar_image_ids = similarity_search.find(image)
    return similar_image_ids


def get_image_paths(prod_ids):
    csv_path = './gallery.csv'  # Replace with the actual path
    data = pd.read_csv(csv_path)
    image_paths = []

    for i, prod_id in enumerate(prod_ids):
        row = data[data['seller_img_id'] == prod_id]
        
        if not row.empty:
            image_path = './' + row.iloc[0]['img_path']
            print(image_path)
            image_paths.append(image_path)

    return image_paths

def main():
    st.title("Image Similarity Search")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()
        
        # Save the uploaded image to the temporary directory
        temp_image_path = os.path.join(temp_dir.name, "uploaded_image.jpg")
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_image.read())
        
        # Process the uploaded image and get similar image IDs
        # similar_image_ids = [572, 66, 674, 59, 917, 860, 111, 24, 935, 594, 166, 599, 994, 246, 1025, 38, 1051, 355, 584, 160, 801, 1065, 879, 1032, 223, 591, 521, 191, 874, 180, 953, 616, 603, 343, 564, 425, 672, 891, 649, 235, 797, 283, 906, 927, 888, 610, 858, 386, 63, 411, 338, 82, 931, 456, 811, 667, 207, 360, 510, 567, 449, 700, 989, 454, 398, 841, 626, 183, 248, 740, 288, 929, 914, 991, 546, 242, 798, 13, 303, 1028, 955, 709, 894, 754, 963, 687, 569, 554, 671, 821, 469, 587, 910, 486, 430, 20, 402, 652, 775, 415, 418, 336, 1001, 765, 302, 243, 1049, 453, 299, 1059, 68, 437, 990, 377, 802, 716, 34, 333, 820, 875, 119, 729, 195, 1042, 960, 833, 311, 134, 638, 525, 541, 838, 620, 435, 170, 733, 785, 136, 768, 915, 764, 461, 125, 61, 392, 362, 852, 265, 933, 393, 176, 943, 421, 606, 444, 214, 3, 190, 113, 977, 738, 509, 364, 383, 518, 792, 157, 1039, 384, 556, 257, 48, 574, 272, 394, 121, 719, 196, 714, 407, 330, 604, 405, 950, 749, 179, 692, 1009, 45, 332, 395, 463, 549, 500, 999, 896, 781, 1015, 93, 109, 358, 76, 98, 1017, 1, 835, 698, 310, 531, 527, 233, 653, 632, 46, 1035, 120, 998, 347, 847, 192, 936, 787, 688, 145, 1024, 537, 842, 92, 930, 866, 241, 708, 880, 285, 782, 773, 623, 497, 645, 350, 624, 640, 208, 636, 598, 966, 803, 854, 857, 69, 292, 379, 67, 374, 324, 573, 689, 193, 177, 559, 968, 941, 357, 483, 538, 329, 669, 1000, 832, 123, 503, 648, 29, 387, 1048, 685, 739, 261, 947, 830, 419, 266, 137, 596, 641, 328, 1063, 149, 8, 426, 490, 693, 158, 651, 516, 926, 54, 762, 14, 600, 165, 440, 776, 267, 73, 178, 979, 720, 16, 133, 978, 872, 657, 725, 334, 980, 10, 932, 460, 9, 519, 1036, 423, 268, 751, 694, 416, 681, 194, 647, 103, 959, 517, 245, 885, 167, 181, 142, 331, 139, 954, 236, 65, 1014, 529, 1047, 318, 851, 115, 1064, 100, 856, 255, 105, 84, 508, 809, 560, 274, 586, 710, 297, 705, 200, 767, 1013, 351, 791, 436, 388, 80, 704, 993, 230, 595, 209, 315, 399, 683, 296, 99, 827, 25, 766, 889, 639, 467, 1054, 146, 156, 1040, 919, 378, 487, 222, 923, 981, 582, 789, 492, 40, 148, 724, 478, 579, 91, 761, 253, 307, 618, 489, 369, 558, 249, 870, 723, 555, 741, 628, 1030, 676, 232, 210, 281, 221, 615, 597, 682, 504, 522, 155, 673, 795, 871, 228, 459, 769, 887, 848, 342, 844, 1010, 202, 715, 406, 151, 434, 630, 892, 951, 552, 199, 1033, 477, 97, 902, 613, 886, 530, 185, 397, 934, 354, 414, 964, 1038, 883, 677, 132, 11, 381, 956, 822, 64, 264, 74, 666, 605, 513, 198, 340, 206, 635, 326, 42, 498, 697, 128, 1056, 41, 925, 804, 44, 114, 213, 774, 512, 429, 143, 86, 859, 536, 884, 718, 308, 301, 263, 625, 928, 722, 742, 717, 87, 533, 735, 75, 957, 938, 973, 562, 1057, 12, 107, 643, 561, 169, 108, 217, 837, 70, 433, 290, 732, 188, 571, 836, 352, 1062, 110, 164, 237, 992, 913, 607, 658, 543, 779, 763, 696, 580, 229, 646, 771, 901, 126, 1026, 608, 473, 135, 252, 501, 862, 588, 855, 422, 102, 482, 112, 197, 439, 1052, 601, 287, 1002, 916, 373, 464, 970, 984, 976, 701, 755, 168, 918, 27, 578, 897, 320, 882, 259, 634, 380, 280, 853, 258, 1044, 275, 577, 731, 493, 987, 922, 152, 410, 661, 1034, 909, 451, 129, 15, 772, 593, 458, 312, 26, 1027, 391, 592, 921, 53, 1016, 945, 808, 346, 104, 659, 71, 339, 824, 427, 940, 551, 747, 622, 314, 238, 304, 566, 58, 309, 1004, 800, 22, 828, 1029, 466, 187, 325, 750, 986, 89, 576, 412, 511, 565, 77, 447, 908, 777, 668, 62, 470, 730, 203, 507, 363, 1043, 295, 289, 972, 468, 438, 371, 21, 670, 868, 317, 877, 479, 370, 51, 770, 590, 996, 1045, 441, 818, 420, 890, 163, 713, 173, 6, 849, 1050, 602, 31, 282, 234, 982, 39, 401, 589, 813, 240, 1053, 675, 760, 544, 757, 961, 937, 323, 7, 337, 4, 850, 665, 985, 826, 372, 400, 575, 376, 737, 550, 327, 1018, 825, 727, 35, 144, 495, 706, 172, 539, 481, 997, 389, 244, 409, 1021, 322, 817, 131, 284, 920, 748, 506, 581, 881, 455, 480, 286, 942, 619, 834, 864, 726, 313, 893, 47, 520, 294, 212, 496, 161, 815, 905, 690, 159, 843, 707, 535, 349, 736, 969, 239, 30, 57, 1066, 796, 162, 43, 758, 356, 171, 457, 788, 153, 988, 861, 17, 614, 502, 5, 783, 814, 56, 417, 1023, 345, 617, 974, 1031, 545, 702, 907, 499, 95, 799, 361, 367, 291, 831, 939, 445, 404, 585, 52, 184, 612, 33, 94, 316, 746, 1005, 0, 204, 79, 794, 650, 475, 472, 319, 19, 869, 903, 839, 276, 548, 523, 446, 965, 462, 784, 656, 1060, 846, 116, 816, 609, 269, 703, 679, 1011, 975, 655, 78, 911, 344, 450, 32, 895, 247, 413, 211, 396, 72, 1058, 944, 219, 36, 256, 443, 664, 807, 189, 138, 130, 744, 81, 1008, 1020, 873, 878, 432, 491, 1006, 534, 553, 876, 904, 60, 474, 485, 442, 359, 271, 278, 505, 484, 88, 226, 55, 542, 390, 583, 488, 778, 983, 660, 863, 912, 752, 37, 23, 899, 967, 805, 348, 96, 335, 526, 375, 205, 366, 1003, 306, 85, 637, 629, 695, 1037, 118, 250, 924, 793, 721, 691, 341, 845, 471, 540, 216, 254, 90, 227, 154, 277, 431, 867, 122, 174, 127, 231, 900, 547, 448, 712, 465, 786, 300, 611, 865, 83, 756, 699, 958, 365, 117, 270, 840, 514, 627, 305, 684, 949, 298, 743, 279, 563, 224, 745, 273, 218, 678, 971, 806, 952, 631, 1012, 532, 753, 686, 1055, 680, 2, 734, 711]
        
        target_size = (224, 280)  # Size to resize the images

        search_image = read_image(temp_image_path)

        resized_search_image = Image.fromarray(search_image).resize(target_size)
                    
        st.image(resized_search_image, caption="Input Image", use_column_width=False)

#       similar_image_ids = get_similar_images(temp_image_path)
        client = Client("https://thenujan-vpr-deploy.hf.space/")
        result = client.predict(
                        temp_image_path,	# str (filepath or URL to image) in 'image' Image component
                        api_name="/predict"
        )

        with open(result, 'r') as json_file:
            data = json.load(json_file)

        similar_image_ids = data['similar_image_ids'][0]

        similar_image_paths = get_image_paths(similar_image_ids)

        st.write(f"Found {len(similar_image_ids)} similar images.")

        images_per_page = 20
        num_pages = (len(similar_image_ids) + images_per_page - 1) // images_per_page

        page_num = st.slider("Select Page", min_value=1, max_value=num_pages)

        start_idx = (page_num - 1) * images_per_page
        end_idx = min(start_idx + images_per_page, len(similar_image_ids))

        images_per_row = 4
        

        for i in range(start_idx, end_idx, images_per_row):
            row_images = similar_image_paths[i:i + images_per_row]
            
            # Display images side by side in rows
            row = st.columns(images_per_row)
            
            for j, similar_image_path in enumerate(row_images):
                if os.path.exists(similar_image_path):
                    similar_image = read_image(similar_image_path)
                    
                    # Resize the image to target size
                    resized_image = Image.fromarray(similar_image).resize(target_size)
                    
                    # Display resized images with full width
                    row[j].image(resized_image, caption=similar_image_path, use_column_width=True)
                else:
                    st.write(f"Image not found: {similar_image_path}")

if __name__ == "__main__":
    main()
