import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processes CSV data and creates text chunks for embeddings.

    Why: RAG needs context-rich text chunks. We transform structured CSV data
    into natural language descriptions that capture relationships and enable
    semantic search.
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and validate CSV data"""
        try:
            self.df = pd.read_csv(self.csv_path)
            logger.info(f"Loaded {len(self.df)} rows from {self.csv_path}")
            logger.info(f"Columns: {list(self.df.columns)}")
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise

    def clean_data(self) -> pd.DataFrame:
        """
        Clean and sanitize data.

        Why: Remove nulls, standardize formats, handle data quality issues
        before embedding generation.
        """
        df_clean = self.df.copy()

        # Remove rows with missing values
        df_clean = df_clean.dropna()

        # Standardize column names (remove BOM, whitespace)
        df_clean.columns = df_clean.columns.str.strip().str.replace('\ufeff', '')

        # Convert numeric columns
        if 'Quantity (KG)' in df_clean.columns:
            df_clean['Quantity (KG)'] = pd.to_numeric(df_clean['Quantity (KG)'], errors='coerce')
        if 'Spend (USD)' in df_clean.columns:
            df_clean['Spend (USD)'] = pd.to_numeric(df_clean['Spend (USD)'], errors='coerce')

        # Calculate derived metrics for richer context
        if 'Spend (USD)' in df_clean.columns and 'Quantity (KG)' in df_clean.columns:
            df_clean['Price_per_KG'] = df_clean['Spend (USD)'] / df_clean['Quantity (KG)']

        logger.info(f"Cleaned data: {len(df_clean)} rows")
        return df_clean

    def create_text_chunks(self) -> List[Dict]:
        """
        Convert each row into a rich text chunk with metadata.

        Why: Transform structured data into natural language that embeddings
        can understand. Include multiple perspectives (supplier view, cost view,
        quantity view) to improve retrieval for various query types.
        """
        df_clean = self.clean_data()
        chunks = []

        for idx, row in df_clean.iterrows():
            # Create multiple text representations for better retrieval

            # Main description
            main_text = (
                f"Commodity: {row['Commodity']}. "
                f"Top Supplier: {row['Top Supplier']}. "
                f"Quantity Purchased: {row['Quantity (KG)']} kilograms. "
                f"Total Spend: ${row['Spend (USD)']:,.2f} USD. "
                f"Price per kilogram: ${row['Price_per_KG']:.2f}."
            )

            # Supplier-focused view
            supplier_text = (
                f"{row['Top Supplier']} supplies {row['Commodity']}, "
                f"with {row['Quantity (KG)']} kg purchased for ${row['Spend (USD)']:,.2f}."
            )

            # Cost analysis view
            cost_text = (
                f"The spend on {row['Commodity']} is ${row['Spend (USD)']:,.2f}, "
                f"sourced from {row['Top Supplier']} at ${row['Price_per_KG']:.2f} per kg."
            )

            # Combined comprehensive text for embedding
            combined_text = f"{main_text} {supplier_text} {cost_text}"

            chunk = {
                "id": f"row_{idx}",
                "text": combined_text,
                "metadata": {
                    "commodity": row['Commodity'],
                    "supplier": row['Top Supplier'],
                    "quantity_kg": float(row['Quantity (KG)']),
                    "spend_usd": float(row['Spend (USD)']),
                    "price_per_kg": float(row['Price_per_KG']),
                    "row_index": int(idx)
                }
            }
            chunks.append(chunk)

        logger.info(f"Created {len(chunks)} text chunks")
        return chunks

    def get_summary_stats(self) -> Dict:
        """Get summary statistics for context"""
        df_clean = self.clean_data()

        return {
            "total_commodities": len(df_clean),
            "total_spend": float(df_clean['Spend (USD)'].sum()),
            "total_quantity": float(df_clean['Quantity (KG)'].sum()),
            "avg_price_per_kg": float(df_clean['Price_per_KG'].mean()),
            "commodities": df_clean['Commodity'].tolist(),
            "suppliers": df_clean['Top Supplier'].tolist()
        }
