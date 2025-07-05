from generate_data import SyntheticColumnMappingDataGenerator
import json

def main():
    generator = SyntheticColumnMappingDataGenerator()
    training_data = generator.save_training_data()
    print("\nTraining data generation complete!")
    print(f"Total examples: {len(training_data)}")
    print("\nExample training instance:")
    print(json.dumps(training_data[0], indent=2))


if __name__ == "__main__":
    main()
