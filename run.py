from market import app,db
from sqlalchemy import text  # Required for raw SQL execution

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    with app.app_context():
        # Don't create tables if they exist
        try:
            # Proper way to execute raw SQL in SQLAlchemy 2.0+
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("\n=== DATABASE CONNECTION SUCCESS===\n")
                result.close()  # Explicitly close the result
        except Exception as e:
            print(f"\n=== DATABASE CONNECTION FAILED===")
            print(f"Database connection failed: {str(e)}\n")
            exit(1)
    app.run(debug=True)