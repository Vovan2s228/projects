"""
Character classifier
usecase: python stv_classifier.py test.csv

Please make sure to install all the prerequisite requirements first.
"""

import sys
import csv
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from sklearn import neighbors

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import StandardScaler

def read_train_data_csv(filename):
    data_dict = {}
    img_paths = []
    labels = []
    with open(filename, 'r')  as train_csv:
        reader = csv.reader(train_csv)
        next(reader, None) # skip the csv header
        for rows in reader:
            img_paths.append(rows[0])
            labels.append(rows[1])
        return img_paths, labels


def read_test_data_csv(filename):
    data_dict = {}
    img_paths = []
    with open(filename, 'r')  as train_csv:
        reader = csv.reader(train_csv)
        next(reader, None) # skip the csv header
        for rows in reader:
            img_paths.append(rows[0])
        return img_paths

def load_images(img_paths):
    imgs = []
    for path in img_paths:
        img = io.imread(path, as_gray=True)
        img_np = np.array(img[0], dtype=float)
        imgs.append(img_np)
    return imgs

def get_fft(img):
    z = np.fft.fft2(img) # calculates FFT of image
    q = np.fft.fftshift(z) # shifts center to u=0, v=0
    mag = np.absolute(q) # magnitude spectrum
    phase = np.angle(q) # phase spectrum
    return mag, phase

def box_feature(mag, start_x=0, start_y=0, end_x=400, end_y=640):
    total_mag = 0
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            power = mag[x,y]*mag[x,y]
            total_mag += power
    return total_mag

def get_fft_dataset(ims):
    mags = []
    phases = []
    for im in ims:
        mag, phase = get_fft(im)
        mags.append(mag)
        phases.append(phase)
    return mags, phases

def get_features(mags, phases):
    features = np.zeros((len(mags), 10))
    for i in range(len(mags)):
        mag = mags[i]
        phase = phases[i]
        height, width = mag.shape
        mag_shifted = np.fft.fftshift(mag)
        phase_shifted = np.fft.fftshift(phase)

        #for magnitudes
        u = np.arange(-width//2, width//2)
        v = np.arange(-height//2, height//2)
        U, V = np.meshgrid(u, v)
        Theta = np.arctan2(V, U)
        total_magnitude = np.sum(mag_shifted) + 0.000000001

        central_region_size = 0.1
        cx, cy = width // 2, height // 2
        low_freq_region_size = int(central_region_size * min(width, height) // 2)
        low_freq_mask = np.zeros_like(mag_shifted)
        low_freq_mask[cy - low_freq_region_size : cy + low_freq_region_size,
                      cx - low_freq_region_size : cx + low_freq_region_size] = 1
        low_freq_energy = np.sum(mag_shifted * low_freq_mask)

        vertical_mask = ((Theta >= -np.pi/8) & (Theta <= np.pi/8)) | ((Theta >= 7*np.pi/8) | (Theta <= -7*np.pi/8))
        horizontal_mask = ((Theta >= 3*np.pi/8) & (Theta <= 5*np.pi/8)) | ((Theta <= -3*np.pi/8) & (Theta >= -5*np.pi/8))
        diagonal_mask = ((Theta >= np.pi/8) & (Theta <= 3*np.pi/8)) | ((Theta <= -5*np.pi/8) & (Theta >= -7*np.pi/8))
        other_diagonal_mask = ((Theta >= -3*np.pi/8) & (Theta <= -np.pi/8)) | ((Theta >= 5*np.pi/8) & (Theta <= 7*np.pi/8))

        vertical_energy = np.sum(mag_shifted * vertical_mask)
        horizontal_energy = np.sum(mag_shifted * horizontal_mask)
        diagonal_energy = np.sum(mag_shifted * diagonal_mask)
        other_diagonal_energy = np.sum(mag_shifted * other_diagonal_mask)

        features[i, 0] = low_freq_energy / total_magnitude
        features[i, 1] = vertical_energy / total_magnitude
        features[i, 2] = horizontal_energy / total_magnitude
        features[i, 3] = diagonal_energy / total_magnitude
        features[i, 4] = other_diagonal_energy / total_magnitude

        #for phases
        def circular_mean(angle_array):
            return np.angle(np.sum(np.exp(1j * angle_array)))

        low_freq_phase_values = phase_shifted * low_freq_mask
        low_freq_phase = circular_mean(low_freq_phase_values[low_freq_mask == 1])
        vertical_phase_values = phase_shifted * vertical_mask
        vertical_phase = circular_mean(vertical_phase_values[vertical_mask])
        horizontal_phase_values = phase_shifted * horizontal_mask
        horizontal_phase = circular_mean(horizontal_phase_values[horizontal_mask])
        diagonal_phase_values = phase_shifted * diagonal_mask
        diagonal_phase = circular_mean(diagonal_phase_values[diagonal_mask])
        other_diagonal_phase_values = phase_shifted * other_diagonal_mask
        other_diagonal_phase = circular_mean(other_diagonal_phase_values[other_diagonal_mask])

        features[i, 5] = low_freq_phase / np.pi
        features[i, 6] = vertical_phase / np.pi
        features[i, 7] = horizontal_phase / np.pi
        features[i, 8] = diagonal_phase / np.pi
        features[i, 9] = other_diagonal_phase / np.pi

    return features

def plot_fft(mag, phase):
    plt.subplot(1,2,1)
    plt.imshow(np.log10(abs(mag)+1), cmap='gray')
    plt.title('Magnitude')
    plt.subplot(1,2,2)
    plt.imshow(phase, cmap='gray')
    plt.title('Phase')
    plt.show()

def main():
    test_csv = sys.argv[1]

    train_img_paths, train_labels = read_train_data_csv('train.csv')
    test_img_paths = read_test_data_csv(test_csv)

    train_imgs = load_images(train_img_paths)
    test_imgs = load_images(test_img_paths)

    mags, phases = get_fft_dataset(train_imgs)
    test_mags, test_phases = get_fft_dataset(test_imgs)

    # plot_fft(mags[0], phases[0])  # Plots an example of magnitude and phase

    train_features = get_features(mags, phases)
    test_features = get_features(test_mags, test_phases)

    scaler = StandardScaler()
    train_features = scaler.fit_transform(train_features)
    test_features = scaler.transform(test_features)

    clf = neighbors.KNeighborsClassifier(n_neighbors=3)
    clf.fit(train_features, train_labels)

    predictions = clf.predict(test_features)
    print("Predictions for test images:", predictions)

    predictions_file = test_csv.replace('.csv', '_predictions.csv')
    with open(predictions_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['image_path', 'prediction'])
        for i, pred in enumerate(predictions):
            writer.writerow([test_img_paths[i], pred])
    
    train_predictions = clf.predict(train_features)
    train_accuracy = accuracy_score(train_labels, train_predictions)
    print("Training Accuracy:", train_accuracy)

    scores = cross_val_score(clf, train_features, train_labels, cv=5)
    print("Cross-validation scores:", scores)
    print("Average cross-validation score:", np.mean(scores))

    cm = confusion_matrix(train_labels, train_predictions, labels=['S', 'T', 'V'])
    print("Confusion Matrix:\n", cm)


if __name__ == "__main__":
    main()
