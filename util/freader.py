class FileReader:
  def __init__(self, file_path):
        self.file_path = file_path

  def read(self, process):
      with open(self.file_path, "r", encoding="utf-8") as self.inputFile:  # Set encoding to 'utf-8'
          for line in self.inputFile:
              process(line)

  def stop(self):
    self.inputFile.close()


def readAsString(filePath):
  return "\n".join(readAsList(filePath))

def readAsList(filePath):
  r = FileReader(filePath)
  res = [ ]
  r.read(lambda l: res.append(l))
  return res
