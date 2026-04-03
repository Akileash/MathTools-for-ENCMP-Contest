import matrix_solver
import revolution_visualizer


def print_main_menu():
    print("\n=== Math Tools Final Main Menu ===")
    print("1) Advanced Matrix Solver")
    print("2) Solids of Revolution 3D Visualizer")
    print("0) Exit")


def main():
    while True:
        print_main_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\nOpening Advanced Matrix Solver...")
            matrix_solver.main()
        elif choice == "2":
            print("\nOpening Solids of Revolution 3D Visualizer...")
            revolution_visualizer.main()
        elif choice == "0":
            print("Exiting Math Tools.")
            break
        else:
            print("Invalid option. Please enter 1, 2, or 0.")


if __name__ == "__main__":
    main()
