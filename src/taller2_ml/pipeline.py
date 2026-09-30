"""Pipeline reproducible de clasificación usando el conjunto Iris."""

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_pipeline() -> Pipeline:
    """Construye el preprocesamiento y el clasificador en una sola tubería."""
    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=500, random_state=42)),
        ]
    )


def main() -> None:
    """Entrena el pipeline y muestra una métrica sencilla de evaluación."""
    dataset = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        dataset.data,
        dataset.target,
        test_size=0.25,
        random_state=42,
        stratify=dataset.target,
    )

    model = build_pipeline()
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Dataset: Iris ({len(dataset.data)} filas, {len(dataset.feature_names)} variables)")
    print(f"Exactitud en prueba: {accuracy:.3f}")
    print(f"Clases: {', '.join(dataset.target_names)}")


if __name__ == "__main__":
    main()
