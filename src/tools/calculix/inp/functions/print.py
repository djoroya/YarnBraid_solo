def print(self, file):
    # Open the file for writing
    file = open(file, 'w')

    # Define the sections to print
    sections = [self.nodes]   + \
                self.elements + \
                self.nsets + \
                self.elsets   +\
                self.elsetsofelsets + \
                self.surfaces + \
                self.equations + \
                self.ties + \
                self.surface_interactions +\
                self.contacts + \
                self.materials + \
                self.solid_sections

    # Write each section to the file
    for section in sections:
        section_text = section.print().replace('\r', '')
        file.write(section_text + '\n')

    # Close the file
    file.close()