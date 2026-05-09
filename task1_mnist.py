"""
CCS 2226 Foundations of AI - 2026
Task One – MNIST Dataset
(a) Download MNIST Dataset
(b) Write a program to distinguish digits 0–9 using MNIST dataset
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

# ─────────────────────────────────────────────
# (a) Download & Load the MNIST Dataset
# ─────────────────────────────────────────────
print("=" * 55)
print("(a) Downloading and Loading MNIST Dataset...")
print("=" * 55)

(X_train, y_train), (X_test, y_test) = mnist.load_data()

print(f"Training images shape : {X_train.shape}")   # (60000, 28, 28)
print(f"Training labels shape : {y_train.shape}")   # (60000,)
print(f"Test images shape     : {X_test.shape}")    # (10000, 28, 28)
print(f"Test labels shape     : {y_test.shape}")    # (10000,)
print(f"Pixel value range     : {X_train.min()} – {X_train.max()}")
print(f"Classes (digits)      : {np.unique(y_train)}")

# ─────────────────────────────────────────────
# Visualise a Sample of Each Digit (0–9)
# ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
fig.suptitle("MNIST Sample Images – One per Digit (0–9)", fontsize=14, fontweight="bold")

for digit in range(10):
    idx = np.where(y_train == digit)[0][0]          # first occurrence
    ax  = axes[digit // 5][digit % 5]
    ax.imshow(X_train[idx], cmap="gray")
    ax.set_title(f"Digit: {digit}", fontsize=11)
    ax.axis("off")

plt.tight_layout()
plt.savefig("mnist_samples.png", dpi=120)
print("\nSample image grid saved → mnist_samples.png")

# ─────────────────────────────────────────────
# (b) Build a Model to Distinguish Digits 0–9
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("(b) Building Digit Classification Model...")
print("=" * 55)

# --- Pre-processing ---
NUM_CLASSES = 10

# Normalise pixel values to [0, 1]
X_train_norm = X_train.astype("float32") / 255.0
X_test_norm  = X_test.astype("float32")  / 255.0

# Flatten 28×28 images to 784-element vectors
X_train_flat = X_train_norm.reshape(-1, 784)
X_test_flat  = X_test_norm.reshape(-1, 784)

# One-hot encode labels
y_train_ohe  = keras.utils.to_categorical(y_train, NUM_CLASSES)
y_test_ohe   = keras.utils.to_categorical(y_test,  NUM_CLASSES)

# --- Model Architecture ---
model = keras.Sequential(
    [
        keras.Input(shape=(784,)),
        layers.Dense(256, activation="relu",    name="hidden_layer_1"),
        layers.Dropout(0.3,                     name="dropout_1"),
        layers.Dense(128, activation="relu",    name="hidden_layer_2"),
        layers.Dropout(0.2,                     name="dropout_2"),
        layers.Dense(NUM_CLASSES, activation="softmax", name="output_layer"),
    ],
    name="MNIST_Digit_Classifier",
)

model.summary()

# --- Compile ---
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# --- Train ---
print("\nTraining the model (5 epochs)...")
history = model.fit(
    X_train_flat, y_train_ohe,
    epochs=5,
    batch_size=128,
    validation_split=0.1,
    verbose=1,
)

# --- Evaluate ---
print("\n--- Evaluation on Test Set ---")
test_loss, test_acc = model.evaluate(X_test_flat, y_test_ohe, verbose=0)
print(f"Test Loss     : {test_loss:.4f}")
print(f"Test Accuracy : {test_acc * 100:.2f}%")

# --- Predict and Show Results ---
predictions   = model.predict(X_test_flat, verbose=0)
pred_labels   = np.argmax(predictions, axis=1)

fig2, axes2 = plt.subplots(2, 5, figsize=(14, 6))
fig2.suptitle(
    f"Model Predictions on Test Digits 0–9  |  Accuracy: {test_acc*100:.2f}%",
    fontsize=13, fontweight="bold",
)

for digit in range(10):
    idx  = np.where(y_test == digit)[0][0]
    pred = pred_labels[idx]
    conf = predictions[idx][pred] * 100
    ax   = axes2[digit // 5][digit % 5]
    ax.imshow(X_test[idx], cmap="gray")
    color = "green" if pred == digit else "red"
    ax.set_title(f"True: {digit}  Pred: {pred}\nConf: {conf:.1f}%",
                 fontsize=10, color=color)
    ax.axis("off")

plt.tight_layout()
plt.savefig("mnist_predictions.png", dpi=120)
print("Prediction grid saved → mnist_predictions.png")

# --- Training Curves ---
fig3, (ax_l, ax_a) = plt.subplots(1, 2, figsize=(12, 4))
fig3.suptitle("Training History", fontsize=13, fontweight="bold")

ax_l.plot(history.history["loss"],     label="Train Loss")
ax_l.plot(history.history["val_loss"], label="Val Loss")
ax_l.set_title("Loss per Epoch")
ax_l.set_xlabel("Epoch")
ax_l.set_ylabel("Loss")
ax_l.legend()

ax_a.plot(history.history["accuracy"],     label="Train Accuracy")
ax_a.plot(history.history["val_accuracy"], label="Val Accuracy")
ax_a.set_title("Accuracy per Epoch")
ax_a.set_xlabel("Epoch")
ax_a.set_ylabel("Accuracy")
ax_a.legend()

plt.tight_layout()
plt.savefig("mnist_training_curves.png", dpi=120)
print("Training curves saved → mnist_training_curves.png")

print("\nTask One complete!")
