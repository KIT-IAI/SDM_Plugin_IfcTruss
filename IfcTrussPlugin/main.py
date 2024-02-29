import ifcdb
import ifctruss
import pandas as pd
import wx
import IfcTrussDialogImpl

def get_nodes_from_ifcdb(document, nodes_dict):

    node_entities = document.get_entities_by_type("IfcStructuralPointConnection")

    node_list = []
    coordinate_x_list = []
    coordinate_y_list = []
    coordinate_z_list = []
    translational_x_list = []
    translational_y_list = []
    translational_z_list = []
    
    node_index = 0
    
    for entity in node_entities:
      
        node_index += 1

        node_list.append(node_index)
        
        nodes_dict.update({entity.guid : node_index})
        
        geometry = entity.get_geometry()

        if (geometry.type == "Vertex"):
            coordinate_x_list.append(geometry.data[1][0])
            coordinate_y_list.append(geometry.data[1][1])
            coordinate_z_list.append(geometry.data[1][2])
  
        attributes_dict = entity.get_attributes()

        boundary_condition_dict = attributes_dict.get('AppliedCondition')
        
        if boundary_condition_dict != None:
            translational_x_list.append(int(boundary_condition_dict.get('TranslationalStiffnessX') == 'true'))
            translational_y_list.append(int(boundary_condition_dict.get('TranslationalStiffnessY') == 'true'))
            translational_z_list.append(int(boundary_condition_dict.get('TranslationalStiffnessZ') == 'true'))
    
    nodes = pd.DataFrame({
                          "Node": pd.Series(node_list, dtype=int),
                          "Coordinate_X": pd.Series(coordinate_x_list, dtype=float),
                          "Coordinate_Y": pd.Series(coordinate_y_list, dtype=float),
                          "Coordinate_Z": pd.Series(coordinate_z_list, dtype=float),
                          "Translational_X": pd.Series(translational_x_list, dtype=bool),
                          "Translational_Y": pd.Series(translational_y_list, dtype=bool),
                          "Translational_Z": pd.Series(translational_z_list, dtype=bool)
                         })

    return nodes

def get_bars_from_ifcdb(document, nodes_dict):

    bar_entities = document.get_entities_by_type("IfcStructuralCurveMember")

    bar_list = []
    start_node_list = []
    end_node_list = []
    cross_sectional_area_list = []
    modulus_of_elasticity__list = []
    
    bar_index = 0

    for entity in bar_entities:

        bar_index += 1
        bar_list.append(bar_index)
        
        relations = entity.get_relations("IfcRelConnectsStructuralMember")

        relation_count = 0
        for relation in relations:
        
            relation_count += 1
            
            attributes_dict = relation.get_attributes()

            related_structural_element = document.get_entity_by_oid(attributes_dict.get('RelatedStructuralConnection'))
            
            if relation_count == 1:
                start_node_list.append(nodes_dict.get(related_structural_element.guid))
                
            if relation_count == 2:
                end_node_list.append(nodes_dict.get(related_structural_element.guid))

        relations = entity.get_relations("IfcRelAssociatesMaterial")

        for relation in relations:

            attributes_dict = relation.get_attributes()

            relating_material_dict = attributes_dict.get('RelatingMaterial')
            
            material_profiles = relating_material_dict.get('MaterialProfiles')
            
            for material_profile_dict in material_profiles:
            
                material_properties_dict = material_profile_dict.get('MaterialProperties')
                
                pset_profile_mechanical_dict = material_properties_dict.get('Pset_ProfileMechanical')

                cross_section_area = pset_profile_mechanical_dict.get('CrossSectionArea')
                cross_sectional_area_list.append(cross_section_area[0])
                
                pset_material_mechanical_dict = material_properties_dict.get('Pset_MaterialMechanical')
                
                young_modulus = pset_material_mechanical_dict.get('YoungModulus')
                modulus_of_elasticity__list.append(young_modulus[0])

    bars = pd.DataFrame({
                         "Bar": pd.Series(bar_list, dtype=int),
                         "Start_node": pd.Series(start_node_list, dtype=int),
                         "End_node": pd.Series(end_node_list, dtype=int),
                         "Cross-sectional_area": pd.Series(cross_sectional_area_list, dtype=float),
                         "Modulus_of_elasticity": pd.Series(modulus_of_elasticity__list, dtype=float)
                        })

    return bars

def get_point_loads_from_ifcdb(document, nodes_dict):

    point_load_list = []
    node_list = []
    force_x_list = []
    force_y_list = []
    force_z_list = []
    
    point_load_index = 0

    point_load_entities = document.get_entities_by_type("IfcStructuralPointAction")
    
    for entity in point_load_entities:

        point_load_index += 1

        point_load_list.append(point_load_index)
        
        relations = entity.get_relations("IfcRelConnectsStructuralActivity")

        for relation in relations:
        
            attributes_dict = relation.get_attributes()
        
            relating_element = document.get_entity_by_oid(attributes_dict.get('RelatingElement'))
            
            node_list.append(nodes_dict.get(relating_element.guid))
 
        attributes_dict = entity.get_attributes()

        single_force_dict = attributes_dict.get('AppliedLoad')

        if single_force_dict != None:
            force_x_list.append(single_force_dict.get('ForceX'))
            force_y_list.append(single_force_dict.get('ForceY'))
            force_z_list.append(single_force_dict.get('ForceZ'))

    point_loads = pd.DataFrame({
                                "Point_Load": pd.Series(point_load_list, dtype=int),
                                "Node": pd.Series(node_list, dtype=int),
                                "Force_X": pd.Series(force_x_list, dtype=float),
                                "Force_Y": pd.Series(force_y_list, dtype=float),
                                "Force_Z": pd.Series(force_z_list, dtype=float)
                               })
    return point_loads

def truss_calculation():

    document = ifcdb.get_document()

    document.log_message("IfcTruss calculation")

    nodes_dict = {}

    nodes = get_nodes_from_ifcdb(document, nodes_dict)
    bars = get_bars_from_ifcdb(document, nodes_dict)
    point_loads = get_point_loads_from_ifcdb(document, nodes_dict)

    results = ifctruss.solver.direct_stiffness_method(nodes, bars, point_loads)

    app = wx.App(False)
    dlg = IfcTrussDialogImpl.IfcTrussDialogImpl(None)
    dlg.fillGrid(results)
    dlg.ShowModal()
    dlg.Destroy()

truss_calculation()
