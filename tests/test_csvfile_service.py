import os

from src.correios_cep.service.csvfile_service import CSVFileService


def test_csv_file_service_save_and_delete(tmp_path):
    service = CSVFileService(temp_dir=str(tmp_path))

    content = "state,city,Neighborhood,zipcode,street\nMG,Carangola,Alvorada,36803000,"
    filename = "test_postal_codes.csv"

    filepath = service.save(filename=filename, content=content)

    assert os.path.isfile(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        assert f.read() == content

    service.delete(filepath)
    assert not os.path.exists(filepath)

